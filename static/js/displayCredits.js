/**
 * Appends the given Array of course names as an unordered list to the table data entry for the list with the
 * given id
 * @param listId
 * @param credits
 */
function displayCredits(listId, credits) {
    let list = document.getElementById(listId);
    // Remove any existing list items. These may be here from a previous method call.
    console.log("In method displayCredits()");
    console.log(list);
    console.log(list.children);
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }

    // Create a list item for each credited AP course.
    // If there are no credited courses, leave a default message.
    if (credits.length === 0) {
        let list_item = document.createElement("li");
        list_item.textContent = "No applicable credits";
        list.append(list_item);
    } else {
        for (let i = 0; i < credits.length; i++) {
            let list_item = document.createElement("li");
            list_item.textContent = credits[i];
            list.append(list_item);
        }
    }

}
