/**
 * Returns true if the unordered list for the given college is empty; False otherwise. This method is used to prevent
 * duplicate AP courses from being added to the page.
 * @param college
 * @param credits
 */
function isEmpty(college) {
    let listId= college + "_ap" + "_ul";
    return document.getElementById(listId).getElementsByTagName("li").length === 0;
}