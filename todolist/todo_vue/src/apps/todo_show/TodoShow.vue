<template>
    <div class="task-details">
        <a :href="this.tasks_list_url" class="task-link">Task List</a><br/>
        <a :href="this.tasks_update_url" class="task-link">Update Tasks</a><br/>
        <a :href="this.tasks_delete_url" class="task-link">Delete Tasks</a><br/>
        <h1 class="task-name">{{ this.tasks.name }}</h1>
        <div class="tag-list">
            <span v-for="tag in this.tasks.tags" class="tag">{{tag.name}}</span>
        </div>
        <p class="task-description">Description: {{this.tasks.description}}</p>
        <p class="task-date">Date: {{this.convert_date_to_string(this.tasks.date)}}</p>
    </div>
</template>


<script>
export default {
    name: 'App',
    data() {
        return {
            tasks_error: [],
            tasks_id: window.ext_tasks_id,
            tasks_detail_js_url: window.ext_tasks_detail_js_url,
            tasks_list_url: window.ext_tasks_list_url,
            tasks_update_url: window.ext_tasks_update_url,
            tasks_delete_url: window.ext_tasks_delete_url,
            tasks: {},
        }
    },
    methods: {
        get_tasks_info() {
            fetch(this.tasks_detail_js_url, {
                method: "GET",
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(this.assign_tasks)
            .catch(error => {
                console.error('Error loading tasks information:', error)
                this.tasks_error.push("Error when loading tasks information")
            })
        },
        assign_tasks(tasks_json) {
            console.log('JSON', tasks_json)
            this.tasks = tasks_json['task']
            if (this.tasks.date) {
                this.tasks.date = this.convert_date_to_string(this.tasks.date)
            }
        },
        convert_date_to_string(date) {
            if (date) {
                const isoDate = new Date(date).toISOString()
                return isoDate.split('T')[0]
            }
        },
    },
    beforeMount() {
        this.get_tasks_info()
    },
}
</script>
<style scoped>
.task-details {
    padding: 20px;
    border: 2px solid #ccc;
    border-radius: 10px;
    background-color: #f0f0f0;
}

.task-name {
    color: #333;
    font-size: 28px;
    margin-bottom: 20px;
    border-bottom: 2px solid #ccc;
    padding-bottom: 10px;
}

.tag-list {
    margin-bottom: 20px;
}

.tag-list ul {
    list-style-type: none;
    padding: 0;
}

.tag-list li {
    display: inline-block;
    margin-right: 10px;
    background-color: #007bff;
    color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
}

.task-description {
    color: #666;
    margin-bottom: 20px;
}

.task-date {
    color: #666;
    margin-bottom: 20px;
}

.task-links {
    margin-top: 20px;
}

.task-link {
    display: inline-block;
    color: #007bff;
    text-decoration: none;
    margin-right: 10px;
}

.task-link:hover {
    text-decoration: underline;
    color: #0056b3;
}
</style>
