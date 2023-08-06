document.addEventListener("DOMContentLoaded", () => {
    // Get all "navbar-burger" elements
    let navbarBurgers = Array.prototype.slice.call(document.querySelectorAll(".navbar-burger"), 0)
    // Check if there are any navbar burgers
    if (navbarBurgers.length > 0) {
        // Add a click event on each of them
        navbarBurgers.forEach((elem: HTMLElement) => {
            elem.addEventListener("click", () => {
                // Get the target from the "data-target" attribute
                let target = elem.dataset["target"] as string
                let elemTarget = document.getElementById(target)
                if (elemTarget) {
                    // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                    elem.classList.toggle("is-active")
                    elemTarget.classList.toggle("is-active")
                }
            })
        })
    }
})
