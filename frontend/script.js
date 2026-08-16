const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("task-form");
const taskList = document.getElementById("task-list");

let tasks = [];

// Get tasks from backend
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/tasks`);

        if (!response.ok) {
            throw new Error("Failed to load tasks");
        }

        tasks = await response.json();

        localStorage.setItem("tasks", JSON.stringify(tasks));

        renderTasks();
    } catch (error) {
        console.error(error);

        // Cache can be used if backend is unavailable
        tasks = JSON.parse(localStorage.getItem("tasks")) || [];
        renderTasks();
    }
}


// Display tasks
function renderTasks() {
    taskList.innerHTML = "";

    tasks.forEach((task) => {
        const div = document.createElement("div");

        div.className = "task-item";

        const title = document.createElement("span");
        title.textContent = task.title;

        const priority = document.createElement("span");
        priority.textContent = " Priority: " + task.priority;

        const dueDate = document.createElement("span");
        dueDate.textContent = " Due: " + task.due_date;

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";

        editButton.addEventListener("click", () => editTask(task));

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", () => deleteTask(task.id));

        div.appendChild(title);
        div.appendChild(priority);
        div.appendChild(dueDate);
        div.appendChild(editButton);
        div.appendChild(deleteButton);

        taskList.appendChild(div);
    });
}


// Add task
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const titleInput = document.getElementById("title");
    const dueDateInput = document.getElementById("due-date");
    const priorityInput = document.getElementById("priority");

    const title = titleInput.value.trim();

    if (title === "") {
        alert("Please enter task title");
        return;
    }

    const taskData = {
        title: title,
        priority: priorityInput.value,
        due_date: dueDateInput.value,
        project_id: 1
    };

    try {
        const response = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(taskData)
        });

        if (!response.ok) {
            throw new Error("Failed to add task");
        }

        await loadTasks();

        form.reset();

    } catch (error) {
        console.error(error);
        alert("Could not add task");
    }
});


// Edit task
async function editTask(task) {
    const newTitle = prompt("Enter new title", task.title);

    if (!newTitle || newTitle.trim() === "") {
        return;
    }

    const newPriority = prompt(
        "Enter priority: low, medium or high",
        task.priority
    );

    if (!["low", "medium", "high"].includes(newPriority)) {
        alert("Priority must be low, medium or high");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/tasks/${task.id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                title: newTitle.trim(),
                priority: newPriority,
                due_date: task.due_date
            })
        });

        if (!response.ok) {
            throw new Error("Failed to update task");
        }

        await loadTasks();

    } catch (error) {
        console.error(error);
        alert("Could not update task");
    }
}


// Delete task
async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_URL}/tasks/${taskId}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Failed to delete task");
        }

        await loadTasks();

    } catch (error) {
        console.error(error);
        alert("Could not delete task");
    }
}


// Load tasks when page opens
loadTasks();