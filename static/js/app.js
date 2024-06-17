const JSON_HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
};

const NO_PROJECT = {"p_id": -1, "p_name": null, "p_tasks_count": -1}

const NO_TASK = {"t_id": -1, "t_date": null, "t_subject": null, "t_priority": -1, "t_comments": null}

new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    data: {
        projects: [NO_PROJECT],
        p_name: null,
        current_project: NO_PROJECT,
        tasks: [NO_TASK],
        t_subject: null,
        current_subject: null,
        current_task: NO_TASK,
        whoiam: "?",
        task_error: null,
        project_details: false,
        task_details: false,
        is_sqlx: false,
    },
    methods: {
        askWhoIAm() {
            this.whoiam = "drf, django.db, sqlite3, no-npm, vue " + Vue.version
            document.title = 'SDM-Todo'

//            fetch("/api/whoiam")
//                .then(async (resp) => {
//                    if (resp.status === 200) {
//                        this.whoiam = await resp.text()
//                        this.whoiam += ", no-npm, vue " + Vue.version
//                        document.title = 'SDM-Todo'
//                        if (this.whoiam.includes('sqlx')) {
//                            this.is_sqlx = true
//                        }
//                    } else {
//                        let j = await resp.text()
//                        console.log(resp.status + "\n" + j);
//                    }
//                })
//                .catch((reason) => {
//                    console.log(reason)
//                })
        },
        renderProjects() {
            fetch("/api/projects")
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.projects = await resp.json()
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        renderProjectDetails(p_id) {
            this.renderCurrentProject(p_id)
            this.renderProjectTasks(p_id);
            this.project_details = true
            this.task_details = false
        },
        renderCurrentProject(p_id) {
            fetch("/api/projects/" + p_id)
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.current_project = await resp.json()
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        renderProjectTasks(p_id) {
            fetch("/api/projects/" + p_id + "/tasks")
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.tasks = await resp.json()
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
            fetch("/api/tasks/" + t_id)
                .then(async (resp) => {
                    if (resp.status === 200) {
                        let task = await resp.json()
                        this.current_subject = task.t_subject;
                        this.current_task = task;
                        this.task_error = null;
                        this.task_details = true
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        projectCreate() {
            let json = JSON.stringify({"p_name": this.p_name})
            fetch("/api/projects", {
                method: 'post',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 201) {
                        this.renderProjects();
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        projectUpdate() {
            let p_id = this.current_project.p_id
            let json = JSON.stringify(this.current_project)
            fetch("/api/projects/" + p_id, {
                method: 'put',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.renderProjects();
                    } else {
                        let j = await resp.text()
                        alert(resp.status + "\n" + j);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        projectDelete() {
            let p_id = this.current_project.p_id
            fetch("/api/projects/" + p_id, {
                method: 'delete'
            })
                .then(async (resp) => {
                    if (resp.status === 204) {
                        this.project_details = false
                        this.task_details = false
                        this.renderProjects();
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
            let p_id = this.current_project.p_id
            let json = JSON.stringify({"t_subject": this.t_subject})
            fetch("/api/projects/" + p_id + "/tasks", {
                method: 'post',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 201) {
                        this.renderProjects(); // update tasks count
                        this.renderProjectDetails(p_id);
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
            if (!isNaN(this.current_task.t_priority)) {
                this.current_task.t_priority = parseInt(this.current_task.t_priority);
            }
            let json = JSON.stringify(this.current_task)
            let p_id = this.current_project.p_id
            let t_id = this.current_task.t_id
            fetch("/api/tasks/" + t_id, {
                method: 'put',
                headers: JSON_HEADERS,
                body: json
            })
                .then(async (resp) => {
                    if (resp.status === 200) {
                        this.renderProjectTasks(p_id);
                        this.renderTaskDetails(t_id);
                    } else {
                        let text = await resp.text()
                        this.task_error = (resp.status + "\n" + text);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        taskDelete() {
            let p_id = this.current_project.p_id
            let t_id = this.current_task.t_id
            fetch("/api/tasks/" + t_id, {
                method: "delete"
            })
                .then(async (resp) => {
                    if (resp.status === 204) {
                        this.task_details = false
                        this.renderProjects(); // update tasks count
                        this.renderProjectDetails(p_id);
                    } else {
                        let text = await resp.text()
                        alert(resp.status + "\n" + text);
                    }
                })
                .catch((reason) => {
                    console.log(reason)
                })
        },
        hideProjectDetails() {
            this.project_details = false
            this.task_details = false
        },
        hideTaskDetails() {
            this.task_details = false
        },
    },
    created() {
    },
    updated() {
    },
    mounted() { // https://codepen.io/g2g/pen/mdyeoXB
        this.askWhoIAm();
        this.renderProjects();
    },
})