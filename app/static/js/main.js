// Search show toggle in Navbar. (mobile)
let search = document.querySelector("#m_search");
let nav_search = document.querySelector("#m_nav_search");
let search_in = document.querySelector("#search");
search.addEventListener("click", () => {
    if (search_in.style.display == "" && nav_search.style.border == "") {
        search_in.style.display = "inline";
        nav_search.style.border = "1px solid #001427";
    } else {
        search_in.style.display = "";
        nav_search.style.border = "";
    }
});

// Topics Show. (mobile)
let topic_btn = document.querySelector("#m_topic_btn");
let topics_wrapper = document.querySelector("#m_topics_wrapper");
topic_btn.addEventListener("click", () => {
    if ((topics_wrapper.style.backgroundColor = "transparent")) {
        topics_wrapper.style.display = "block";
        topics_wrapper.style.backgroundColor = "rgba(0, 0, 0, 0.2)";
    }
});

// Topics close. (mobile)
let topic_close = document.querySelector("#m_topic_close");
topic_close.addEventListener("click", () => {
    if ((topics_wrapper.style.display = "block")) {
        topics_wrapper.style.display = "none";
    }
});
