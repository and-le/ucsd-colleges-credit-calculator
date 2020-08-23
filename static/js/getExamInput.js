function getExamInput() {
    // Add the checked courses to the array
    const checkBoxes = document.getElementsByClassName("exam_checkbox");
    const scores = document.getElementsByClassName("exam_text");
    let courses = [];
    for (i = 0; i < checkBoxes.length; i++) {
        if (checkBoxes[i].checked) {
            let course = {
                "course": checkBoxes[i].name,
                "score": scores[i].value
            };
            courses.push(course)
        }
    }
    return courses;
}