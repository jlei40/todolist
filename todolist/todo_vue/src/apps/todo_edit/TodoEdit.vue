<template>
    <div>
        <div v-if="form_error">
            <ul>
                <li v-for="(error, index) in form_error">
                    {{error}}
                </li>
            </ul>
        </div>
        <div v-if="form_updated">
            {{ form_updated }}
        </div><br>
            <input type="hidden" name="csrfmiddlewaretoken" v-bind:value="csrf_token">
            <p>
                <label for="id_name">Task Title: </label> &nbsp;
                <input type="text" name="name" v-model="title" maxlength="100"
                required="" id="id_name">
            </p>
            <p>
                <label for="id_homework">Type:</label>&nbsp;
                <select v-model="homework" name="homework"  id="id_homework" style="display:inline-block;padding:1px;">
                    <!-- <option v-for="type in types" :value="type" selected=""></option> -->
                    <option :value="true" >Homework</option>
                    <option :value="false" >Chore</option>
                </select>
            </p>
            <p>
                <label for="id_tags">Tags:</label>
                <select hidden name="tags"  id="id_tags" multiple="">
                    <option v-for="tag in tag_list" :value="tag.id" selected=""></option>
                </select>
                <span v-if="homework">
                    <multiselect v-model="tag_list" :options="tag_list_source.filter(check)" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Choose the tags" label="name" track-by="name"  style="display:inline-block;width: 300px;padding-bottom:10px;padding-left:10px">
                        <template slot="selection" slot-scope="{ values, search, isOpen }"><span class="multiselect__single" v-if="values.length" v-show="!isOpen">{{ values.length }} options selected</span></template>
                    </multiselect>
                </span>
                <span v-if=" homework == false">
                    <multiselect v-model="tag_list" :options="tag_list_source.filter(checkc)" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="Choose the tags" label="name" track-by="name"  style="display:inline-block;width: 300px;padding-bottom:10px;padding-left:10px">
                        <template slot="selection" slot-scope="{ values, search, isOpen }"><span class="multiselect__single" v-if="values.length" v-show="!isOpen">{{ values.length }} options selected</span></template>
                    </multiselect>
                </span>
            </p>
            <p>
                <label for="id_description">Description: </label>&nbsp;
                <input type="hidden" :value="description" name="description" value=""
                maxlength="500" required="" id="id_description">
                <textarea v-model="description" name="description" cols="50" maxlength="5000" rows="3"> </textarea>
            </p>
            <p>
                <label for="id_date">Date:  </label>&nbsp;
                <input type="hidden" name="date" :value="get_date_string" required=""
                id="id_date">
                <VueDatePicker  v-model="date" format="yyyy-MM-dd HH:mm" value="date" style="width:250px;display: inline-block;" :min-date='new Date()'></VueDatePicker>
            </p>
            <button type="submit" class="btn btn-primary"
            @click.prevent="submit_form_fetch"
            :disabled="submitting_form">
                Submit
            </button>
    </div>
    <br><br>
</template>
<script>
import VueDatePicker from '@vuepic/vue-datepicker'; 
import '@vuepic/vue-datepicker/dist/main.css'
import { resolveTransitionHooks } from 'vue';
import Multiselect from 'vue-multiselect'
export default {
    name: 'AppEdit',
    components: {
        VueDatePicker,
        Multiselect,
    },
    data: function() {
        return {
            csrf_token: ext_csrf_token,
            form: ext_form,
            tasks_dico: ext_tasks_dict,
            title: ext_tasks_dict.name,
    	    tag_list_source: (ext_tag_list != undefined) ? ext_tag_list: [],
            homework_tag_source: this.get_homework_tags,
            chore_tag_source: this.get_chore_tags,
            date: this.proceed('date'),
            submitting_form: false,
            form_error: [],
            types: ['Homework', 'Chore'],
            type: null,
            homework: ext_tasks_dict.homework, 
	    	form_updated: "",
            description: ext_tasks_dict.description,
            update_bis_url: ext_update_bis_url,
            tag_list: (ext_tasks_dict.tags != undefined && ext_tasks_dict.tags != null) ? ext_tasks_dict.tags : [],
        }
    },
    methods: {
        check(item){
            return item.homework == true
        },
        checkc(item){
            return item.homework == false
        },
        set(int){
            if (int == 1)
                this.homework = true;
            else if (int == 2)
                this.homework = false;
        },  
        submit_form_fetch(){
            console.log(ext_tasks_dict)
            console.log(this.tag_list)
        	this.form_error = []
        	this.form_updated = ""
        	let formData = new FormData();
        	let form_data = {
	            	'name': this.title,
                    'homework': this.homework,
	            	'description': this.description,
	            	'date': this.get_date_string,
        	}
        	for (var key in form_data) {
            		formData.append(key, form_data[key])
        	}
        	this.tag_list.map(dic => formData.append('tags', dic.id))
        	fetch(this.update_bis_url,
            	{
                	method: "post",
                	body: formData,
                	headers: {'X-CSRFToken': this.csrf_token},
                	credentials: 'same-origin'
            	}
        	).then(function(response) {
            	console.log('response', response)
            	return response.json()}).then(
	            	this.handleResponse).catch(
	                	(error) => {
	                	console.log('error', String(error))
	                	this.form_error=["error"]
    			})
    	},
    	handleResponse(response) {
        	console.log('json response', response)
        	if ('success' in response){
	            	if (response['success'] == true) {
	                	this.form_updated = "tasks has been updated"
	            	} else {
	                	if ('errors' in response){
		                    	for (const [key, value] of Object.entries(response['errors'])) {
		                        	for (const error of value) {
		                            		this.form_error.push(`${key}: ${error}`)
		                        	}
	                    		}
	                	} else {
	                    		this.form_error=["Update failed - An error occurred but do not have more information about it"]
	                	}
	            	}
		} else {
	            	this.form_error=["Update failed - It has been an error on the form request"]
		}
            console.log(this.form_error)
    	},
        submit_form(){
            if (this.submitting_form === true) {
            return;
            }
            this.submitting_form = true
            var form = document.createElement('form');
            form.setAttribute('method', 'post');
            let form_data = {
                'csrfmiddlewaretoken': this.csrf_token,
                'name': this.tasks_dico.name,
                'description': this.tasks_dico.description,
                'date': this.get_date_string,
            }
            console.log('tag_list', this.tag_list)
            console.log("form_data", form_data)
            for (var key in form_data) {
                var html_field = document.createElement('input')
                html_field.setAttribute('type', 'hidden')
                html_field.setAttribute('name', key)
                html_field.setAttribute('value', form_data[key])
                form.appendChild(html_field)
            }
            var tag_field = document.createElement('select')
            tag_field.setAttribute('name', 'tag')
            tag_field.setAttribute('id', 'id_tag')
            tag_field.setAttribute('multiple', '')
            for (var tag of this.tag_list) {
                console.log('tag', tag)
                var option_field = document.createElement('option')
                option_field.setAttribute('value', tag.id)
                option_field.setAttribute('selected', '')
                tag_field.appendChild(option_field)
            }
            form.appendChild(tag_field)
            document.body.appendChild(form);
            form.submit()
        },
        convert_date_to_string(dato){
            const offset = dato.getTimezoneOffset()
            dato = new Date(dato.getTime() - (offset*60*1000))
            console.log('date', dato, dato.toISOString())
            return dato.toISOString()
        },
        proceed(dot){
            if (window.ext_tasks_dict != undefined  ){
                if(dot == 'date'){
                    console.log(this.datify(window.ext_tasks_dict.date))
                    return this.datify(window.ext_tasks_dict.date)
                }
            }
            else{
                return null
            }
        },
        datify(string){
            let dat = new Date(string)
            const offset = dat.getTimezoneOffset()
            dat = new Date(dat.getTime() + (offset*60*1000))
            console.log(dat)
            return dat
        },
    },
    computed: {
        get_homework_tags(){
            this.homework_tag_source = this.tag_list_source.filter(this.check)
        },
        get_chore_tags(){
            this.chore_tag_source = this.tag_list_source.filter(this.checkc)
        },
        get_date_string() {
            if (this.date == null) {
                return ""
            } else {
                return this.convert_date_to_string(this.date)
            }
        },
        
    },
    mounted(){
            this.csrf_token=ext_csrf_token;
            this.tasks_dico=ext_tasks_dict;  
            this.tag_list_source= ext_tag_list;
            this.tag_list = JSON.parse(ext_tasks_dict.tags);
            this.homework = ext_tasks_dict.homework;
    },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>
