const JSON_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
};

const NO_GROUP = {"g_id": -1, "g_name": null, "g_tasks_count": -1}

const NO_TASK = {"t_id": -1, "t_date": null, "t_subject": null, "t_priority": -1, "t_comments": null}

new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    data: {
        groups: null,
        g_name: null,
        current_group: NO_GROUP,
        tasks: null,
        t_subject: null,
        current_task: NO_TASK,
        whoiam: "?",
        task_error: null,
    },
    methods: {
        askWhoIAm() {
            fetch("/whoiam")
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.whoiam = await resp.text()
                    } else {
                        let j = await resp.text()
                        console.log(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        renderGroups() {
            fetch("/groups")
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.$data.groups = await resp.json()
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        renderGroupDetails(g_id) {
            this.renderCurrentGroup(g_id)
            this.renderGroupTasks(g_id);
            showGroupDetails();
            hideTaskDetails();
        },
        renderCurrentGroup(g_id) {
            fetch("/groups/" + g_id)
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.$data.current_group = await resp.json()
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        renderGroupTasks(g_id) {
            fetch("/groups/" + g_id + "/tasks")
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.$data.tasks = await resp.json()
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        renderTaskDetails(t_id) {
            fetch("/tasks/" + t_id)
                .then(async (resp) => {
                    if (resp.status === 200) {
                        let task = await resp.json()
                        let subj = document.getElementById("subj");
                        subj.innerText = task.t_subject;
                        this.$data.current_task = task;
                        this.$data.task_error = null;
                        showTaskDetails();
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        groupCreate() {
            let json = JSON.stringify({"g_name": this.$data.g_name})
            fetch("/groups", {
                method: 'post',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 201) {
                        this.renderGroups();
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        groupUpdate() {
            let g_id = this.$data.current_group.g_id
            let json = JSON.stringify(this.$data.current_group)
            fetch("/groups/" + g_id, {
                method: 'put',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.renderGroups();
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        groupDelete() {
            let g_id = this.$data.current_group.g_id
            fetch("/groups/" + g_id, {
                method: 'delete'
            })
                .then(async (resp) => {
                    if (resp.status === 204) {
                        hideTaskDetails();
                        hideGroupDetails();
                        this.renderGroups();
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        taskCreate() {
            let g_id = this.$data.current_group.g_id
            let json = JSON.stringify({"t_subject": this.$data.t_subject})
            fetch("/groups/" + g_id + "/tasks", {
                method: 'post',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 201) {
                        this.renderGroups(); // update tasks count
                        this.renderGroupDetails(g_id);
                    } else {
                        let text = await resp.text()
                        alert(resp.status + "\n" + text);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        taskUpdate() {
            if (!isNaN(this.$data.current_task.t_priority)) {
                this.$data.current_task.t_priority = parseInt(this.$data.current_task.t_priority);
            }
            let json = JSON.stringify(this.$data.current_task)
            let g_id = this.$data.current_group.g_id
            let t_id = this.$data.current_task.t_id
            fetch("/tasks/" + t_id, {
                method: 'put',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.renderGroupTasks(g_id);
                        this.renderTaskDetails(t_id);
                    } else {
                        let text = await resp.text()
                        this.$data.task_error = (resp.status + "\n" + text);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        taskDelete() {
            let g_id = this.$data.current_group.g_id
            let t_id = this.$data.current_task.t_id
            fetch("/tasks/" + t_id, {
                method: "delete"
            })
                .then(async (resp) => {
                    if (resp.status === 204) {
                        hideTaskDetails();
                        this.renderGroups(); // update tasks count
                        this.renderGroupDetails(g_id);
                    } else {
                        let text = await resp.text()
                        alert(resp.status + "\n" + text);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
    },
    created() {
    },
    updated() {
    },
    mounted() { // https://codepen.io/g2g/pen/mdyeoXB
        //this.askWhoIAm();
        this.renderGroups();
    },
})

function hideTaskDetails() {
    let form = document.getElementById("form_task_details");
    form.style.visibility = "hidden";
}

function showTaskDetails() {
    let form = document.getElementById("form_task_details");
    form.style.visibility = "visible";
}

function hideGroupDetails() {
    let group_details = document.getElementById("group_details");
    group_details.style.visibility = "hidden";
}

function hideGroupDetails2() {
    let group_details = document.getElementById("group_details");
    group_details.style.visibility = "hidden";
    hideTaskDetails();
}

function showGroupDetails() {
    let group_details = document.getElementById("group_details");
    group_details.style.visibility = "visible";
}
