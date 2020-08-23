/**
 * Appends the given Array of course names as an unordered list to the table data entry for the specified college
 * @param college
 * @param credits
 */
function displayCredits(college, credits) {
    let listId= college + "_ap" + "_ul";
    const list = document.getElementById(listId);

    // Create a list item for each credited AP course.
    for (let i = 0; i < credits.length; i++) {
        let list_item = document.createElement("li");
        list_item.textContent = credits[i];
        list.append(list_item);
    }
}