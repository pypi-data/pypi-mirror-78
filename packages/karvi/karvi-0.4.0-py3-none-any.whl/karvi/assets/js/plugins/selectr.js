import Selectr from "mobius1-selectr"

document.addEventListener("DOMContentLoaded", () => {
    // Get all "selectr" elements
    const $selectr = document.querySelectorAll(".selectr")
    const $selectrWidgets = Array.prototype.slice.call($selectr, 0)
    // Check if there are any selectr
    if ($selectrWidgets.length > 0) {
        // Initiate Selectr on each of them
        $selectrWidgets.forEach(el => {
            let htmlClasses = el.attributes.class.value
            let isMultiple = htmlClasses.match("is-multiple") !== null
            let isSearchable = htmlClasses.match("is-searchable") !== null
            let options = {
                searchable: isSearchable,
                multiple: isMultiple
            }
            new Selectr(el, options)
        })
    }
})
