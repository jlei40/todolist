<template>
    <div>
      <div v-if="form_error">
        <ul>
          <li v-for="(error, index) in form_error" :key="index">
            {{ error }}
          </li>
        </ul>
      </div>
      <div v-if="form_updated">{{ form_updated }}</div>
      <br />
      <form @submit.prevent="submit_form_fetch">
        <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token" />
        <p>
          <label for="id_name">Task Title:</label>
          <input type="text" name="name" v-model="title" maxlength="100" required id="id_name" />
        </p>
        <p>
          <label for="id_description">Description:</label>
          <textarea v-model="description" name="description" cols="50" maxlength="5000" rows="3"></textarea>
        </p>
        <p>
          <label for="id_date">Date:</label>
          <VueDatePicker v-model="date" format="yyyy-MM-dd HH:mm" value="date" style="width:250px;display: inline-block;" :min-date="new Date()" />
        </p>
        <button type="submit" class="btn btn-primary" :disabled="submitting_form">Submit</button>
      </form>
    </div>
    <br /><br />
  </template>
  
  <script>
  import VueDatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';
  import Multiselect from 'vue-multiselect';
  
  export default {
    name: 'AppEdit',
    components: {
      VueDatePicker,
      Multiselect,
    },
    data() {
      return {
        csrf_token: ext_csrf_token,
        title: ext_tasks_dict.name,
        description: ext_tasks_dict.description,
        date: new Date(ext_tasks_dict.date),
        submitting_form: false,
        form_error: [],
        form_updated: '',
        update_bis_url: ext_update_bis_url,
      };
    },
    methods: {
      submit_form_fetch() {
        this.form_error = [];
        this.form_updated = '';
        const formData = new FormData();
        formData.append('name', this.title);
        formData.append('description', this.description);
        formData.append('date', this.convert_date_to_string(this.date));
  
        fetch(this.update_bis_url, {
          method: 'post',
          body: formData,
          headers: { 'X-CSRFToken': this.csrf_token },
          credentials: 'same-origin',
        })
          .then((response) => response.json())
          .then(this.handleResponse)
          .catch((error) => {
            console.error('Error:', error);
            this.form_error = ['An error occurred while submitting the form.'];
          });
      },
      handleResponse(response) {
        if ('success' in response) {
          this.form_updated = response.success ? 'Task has been updated' : 'Update failed';
          if (!response.success && response.errors) {
            this.form_error = Object.values(response.errors).flat();
          }
        } else {
          this.form_error = ['Update failed - An error occurred on the server.'];
        }
      },
      convert_date_to_string(dateObj) {
        const offset = dateObj.getTimezoneOffset();
        const correctedDate = new Date(dateObj.getTime() - offset * 60000);
        return correctedDate.toISOString();
      },
    },
  };
  </script>
  
  <style src="vue-multiselect/dist/vue-multiselect.css"></style>
  