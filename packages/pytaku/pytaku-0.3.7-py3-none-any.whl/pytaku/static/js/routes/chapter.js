import { Auth } from "../models.js";
import { LoadingMessage, fullChapterName, Button } from "../utils.js";

const LoadingPlaceholder = {
  view: () => m("h2", [m("i.icon.icon-loader.spin")]),
};

const PendingPlaceholder = {
  view: () => m("h2", [m("i.icon.icon-loader")]),
};

const RetryImgButton = {
  view: (vnode) => {
    return m(Button, {
      text: "Errored. Try again?",
      color: "red",
      onclick: (ev) => {
        const { page } = vnode.attrs;
        page.status = ImgStatus.LOADING;
        // Cheat: append to src so the element's key is
        // different, forcing mithril to redraw.
        // Chose `?` here because it will just be stripped by
        // flask's path parser.
        page.src = page.src.endsWith("?")
          ? page.src.slice(0, -1)
          : page.src + "?";
      },
    });
  },
};

const ImgStatus = {
  LOADING: "loading",
  SUCCEEDED: "succeeded",
  FAILED: "failed",
};

function Chapter(initialVNode) {
  let isLoading = false;
  let chapter = {};
  let loadedPages = [];
  let pendingPages = [];

  function loadNextPage() {
    if (pendingPages.length > 0) {
      loadedPages.push({
        status: ImgStatus.LOADING,
        src: pendingPages.splice(0, 1)[0],
      });
    }
  }

  return {
    oninit: (vnode) => {
      document.title = "Manga chapter";

      isLoading = true;
      m.redraw();

      Auth.request({
        method: "GET",
        url: "/api/chapter/:site/:titleId/:chapterId",
        params: {
          site: vnode.attrs.site,
          titleId: vnode.attrs.titleId,
          chapterId: vnode.attrs.chapterId,
        },
      })
        .then((resp) => {
          chapter = resp;
          document.title = fullChapterName(chapter);
          pendingPages = chapter.pages;
          // start loading pages, 3 at a time:
          loadNextPage();
          loadNextPage();
          loadNextPage();
        })
        .finally(() => {
          isLoading = false;
        });
    },
    view: (vnode) => {
      if (isLoading) {
        return m("div.chapter.content", m(LoadingMessage));
      }

      const { site, titleId } = vnode.attrs;
      const prev = chapter.prev_chapter;
      const next = chapter.next_chapter;
      const buttons = m("div.chapter--buttons", [
        prev
          ? m(
              m.route.Link,
              {
                class: "touch-friendly",
                href: `/m/${site}/${titleId}/${prev.id}`,
              },
              [m("i.icon.icon-chevrons-left"), m("span", "prev")]
            )
          : m(Button, {
              text: "prev",
              icon: "chevrons-left",
              disabled: true,
            }),
        m(
          m.route.Link,
          {
            class: "touch-friendly",
            href: `/m/${site}/${titleId}`,
          },
          [m("i.icon.icon-list"), m("span", " chapter list")]
        ),
        m(
          m.route.Link,
          {
            class: "touch-friendly",
            href: next
              ? `/m/${site}/${titleId}/${next.id}`
              : `/m/${site}/${titleId}`,
            onclick: (ev) => {
              if (Auth.isLoggedIn()) {
                Auth.request({
                  method: "POST",
                  url: "/api/read",
                  body: {
                    read: [
                      {
                        site,
                        title_id: titleId,
                        chapter_id: chapter.id,
                      },
                    ],
                  },
                });
              }
              return true;
            },
          },
          [
            m("span", next ? "next" : "finish"),
            m("i.icon.icon-" + (next ? "chevrons-right" : "check-circle")),
          ]
        ),
      ]);
      return m("div.chapter.content", [
        m("h1", fullChapterName(chapter)),
        buttons,
        m(
          "div",
          {
            class:
              "chapter--pages" +
              (chapter.is_webtoon ? " chapter--webtoon" : ""),
          },
          [
            loadedPages.map((page, pageIndex) =>
              m("div", { key: page.src }, [
                m("img", {
                  src: page.src,
                  style: {
                    display:
                      page.status === ImgStatus.SUCCEEDED ? "block" : "none",
                  },
                  onload: (ev) => {
                    page.status = ImgStatus.SUCCEEDED;
                    loadNextPage();
                  },
                  onerror: (ev) => {
                    page.status = ImgStatus.FAILED;
                    loadNextPage();
                  },
                }),
                page.status === ImgStatus.LOADING
                  ? m(LoadingPlaceholder)
                  : null,
                page.status === ImgStatus.FAILED
                  ? m(
                      "div",
                      { style: { "margin-bottom": ".5rem" } },
                      m(RetryImgButton, { page })
                    )
                  : null,
              ])
            ),
            pendingPages.map((page) => m(PendingPlaceholder)),
          ]
        ),
        buttons,
      ]);
    },
  };
}

export default Chapter;
