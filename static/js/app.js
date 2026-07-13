// Amiral Support Panel — v2.2.0
(function () {
    "use strict";

    /* ---------------------------------------------------------------- Modals */
    function openModal(id) {
        var m = document.getElementById(id);
        if (m) m.classList.add("is-open");
    }
    function closeModal(el) {
        var m = el.closest(".modal");
        if (m) m.classList.remove("is-open");
    }

    document.addEventListener("click", function (e) {
        var opener = e.target.closest("[data-modal-open]");
        if (opener) {
            openModal(opener.getAttribute("data-modal-open"));
            return;
        }
        if (
            e.target.closest("[data-modal-close]") ||
            e.target.classList.contains("modal__overlay")
        ) {
            closeModal(e.target);
        }
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            document.querySelectorAll(".modal.is-open").forEach(function (m) {
                m.classList.remove("is-open");
            });
        }
    });

    /* ------------------------------------------------------------- Edit modal */
    document.querySelectorAll("[data-edit]").forEach(function (btn) {
        btn.addEventListener("click", function () {
            var id = btn.getAttribute("data-id");
            var form = document.getElementById("editForm");
            form.action = "/representatives/" + id + "/edit";
            form.querySelector('[name="name"]').value = btn.getAttribute("data-name");
            form.querySelector('[name="phone"]').value = btn.getAttribute("data-phone");
            form.querySelector('[name="status"]').value = btn.getAttribute("data-status");
            openModal("editModal");
        });
    });

    /* ----------------------------------------------------------- Delete modal */
    document.querySelectorAll("[data-delete]").forEach(function (btn) {
        btn.addEventListener("click", function () {
            var id = btn.getAttribute("data-id");
            var form = document.getElementById("deleteForm");
            form.action = "/representatives/" + id + "/delete";
            document.getElementById("deleteName").textContent =
                btn.getAttribute("data-name");
            openModal("deleteModal");
        });
    });

    /* ------------------------------------------------------- Instant toggle */
    document.querySelectorAll("[data-toggle]").forEach(function (badge) {
        badge.addEventListener("click", function () {
            var id = badge.getAttribute("data-id");
            var card = badge.closest("[data-rep]");
            badge.classList.add("is-busy");

            fetch("/representatives/" + id + "/toggle", {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" },
            })
                .then(function (r) {
                    if (!r.ok) throw new Error("http " + r.status);
                    return r.json();
                })
                .then(function (data) {
                    var online = data.status === 1;
                    badge.classList.toggle("badge--online", online);
                    badge.classList.toggle("badge--offline", !online);
                    badge.querySelector(".badge__label").textContent = online
                        ? "Online"
                        : "Offline";
                    if (card) card.setAttribute("data-status", data.status);
                    applyFilters();
                })
                .catch(function () {
                    alert("Durum güncellenemedi. Sayfayı yenileyip tekrar dene.");
                })
                .finally(function () {
                    badge.classList.remove("is-busy");
                });
        });
    });

    /* --------------------------------------------------------- Search + filter */
    var search = document.getElementById("repSearch");
    var tabs = document.querySelectorAll(".filter-tab");
    var emptyState = document.getElementById("repEmpty");
    var currentFilter = "all";

    function cards() {
        return Array.prototype.slice.call(
            document.querySelectorAll("[data-rep]")
        );
    }

    function applyFilters() {
        var q = (search ? search.value : "").trim().toLowerCase();
        var visible = 0;

        cards().forEach(function (card) {
            var name = (card.getAttribute("data-name") || "").toLowerCase();
            var phone = (card.getAttribute("data-phone") || "").toLowerCase();
            var status = card.getAttribute("data-status");

            var matchesText = !q || name.indexOf(q) > -1 || phone.indexOf(q) > -1;
            var matchesFilter =
                currentFilter === "all" || currentFilter === status;

            if (matchesText && matchesFilter) {
                card.classList.remove("is-hidden");
                visible++;
            } else {
                card.classList.add("is-hidden");
            }
        });

        if (emptyState) {
            emptyState.classList.toggle("is-hidden", visible !== 0);
        }
    }

    if (search) search.addEventListener("input", applyFilters);

    tabs.forEach(function (tab) {
        tab.addEventListener("click", function () {
            tabs.forEach(function (t) {
                t.classList.remove("is-active");
            });
            tab.classList.add("is-active");
            currentFilter = tab.getAttribute("data-filter");
            applyFilters();
        });
    });

    /* ---------------------------------------------------- Drag & drop reorder */
    var grid = document.getElementById("repGrid");
    var dragged = null;

    function getAfterElement(container, y) {
        var els = Array.prototype.slice.call(
            container.querySelectorAll("[data-rep]:not(.is-dragging):not(.is-hidden)")
        );
        var closest = { offset: -Infinity, element: null };
        els.forEach(function (child) {
            var box = child.getBoundingClientRect();
            var offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                closest = { offset: offset, element: child };
            }
        });
        return closest.element;
    }

    function persistOrder() {
        var order = cards().map(function (c) {
            return parseInt(c.getAttribute("data-id"), 10);
        });
        fetch("/representatives/reorder", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ order: order }),
        }).catch(function () {
            /* sessizce yut — sıra DOM'da zaten değişti, sonraki yüklemede düzelir */
        });
    }

    if (grid) {
        grid.addEventListener("dragstart", function (e) {
            var card = e.target.closest("[data-rep]");
            if (!card) return;
            dragged = card;
            card.classList.add("is-dragging");
            if (e.dataTransfer) {
                e.dataTransfer.effectAllowed = "move";
                e.dataTransfer.setData("text/plain", card.getAttribute("data-id"));
            }
        });

        grid.addEventListener("dragover", function (e) {
            if (!dragged) return;
            e.preventDefault();
            var after = getAfterElement(grid, e.clientY);
            if (after == null) {
                grid.appendChild(dragged);
            } else if (after !== dragged) {
                grid.insertBefore(dragged, after);
            }
        });

        grid.addEventListener("dragend", function () {
            if (!dragged) return;
            dragged.classList.remove("is-dragging");
            dragged = null;
            persistOrder();
        });
    }

    /* -------------------------------------------------------- Mobile sidebar */
    var burger = document.getElementById("hamburger");
    var sidebar = document.getElementById("sidebar");
    var backdrop = document.getElementById("sidebarBackdrop");

    function toggleSidebar(open) {
        if (!sidebar) return;
        sidebar.classList.toggle("is-open", open);
        if (backdrop) backdrop.classList.toggle("is-open", open);
    }
    if (burger) {
        burger.addEventListener("click", function () {
            toggleSidebar(!sidebar.classList.contains("is-open"));
        });
    }
    if (backdrop) {
        backdrop.addEventListener("click", function () {
            toggleSidebar(false);
        });
    }

    /* --------------------------------------------------------- Toast dismiss */
    document.querySelectorAll(".toast").forEach(function (toast) {
        setTimeout(function () {
            toast.style.transition = "opacity .3s ease, transform .3s ease";
            toast.style.opacity = "0";
            toast.style.transform = "translateX(20px)";
            setTimeout(function () {
                toast.remove();
            }, 300);
        }, 3500);
    });
})();
