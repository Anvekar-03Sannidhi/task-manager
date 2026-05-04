document.addEventListener("DOMContentLoaded", function () {

    console.log("JS Loaded");

    const btn = document.getElementById("reminder-btn");

    if (!btn) {
        console.log("Button not found ❌");
        return;
    }

    console.log("Button found ✅");

    btn.addEventListener("click", function () {

        const timeInput = document.getElementById("reminder-time").value;

        if (!timeInput) {
            alert("Please select a time!");
            return;
        }

        const now = new Date();
        const [hours, minutes] = timeInput.split(":");

        const reminderTime = new Date();
        reminderTime.setHours(hours, minutes, 0);

        const diff = reminderTime - now;

        if (diff <= 0) {
            alert("Please choose a future time!");
            return;
        }

        alert("Reminder set!");

        setTimeout(() => {
            alert("⏰ Reminder: Check your tasks!");

            if (Notification.permission === "granted") {
                new Notification("Task Reminder", {
                    body: "You have pending tasks!",
                });
            }
        }, diff);

    });

    // Ask notification permission
    if (Notification.permission !== "granted") {
        Notification.requestPermission();
    }

});
