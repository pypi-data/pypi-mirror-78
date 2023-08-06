import Choices from "choices.js"

document.addEventListener("DOMContentLoaded", () => {
    let selectjs = document.querySelectorAll(".selectex")
    selectjs.forEach((elem: HTMLElement) => {
        let choice = new Choices(elem)
    })
})
