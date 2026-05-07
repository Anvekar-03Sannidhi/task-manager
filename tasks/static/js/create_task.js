const taskType = document.getElementById("task-type");
const customBox = document.getElementById("custom-date-box");

taskType.addEventListener("change", () => {

    if (taskType.value === "CUSTOM") {
        customBox.style.display = "block";
    } else {
        customBox.style.display = "none";
    }

});