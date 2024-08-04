<template>
  <div class="dashboard">
    <div class="upload-container">
      <input type="file" @change="handleFileUpload" class="file-input" />
      <button @click="submitFile" class="upload-button">Upload</button>
    </div>
    <Table :columns="columns" :data-source="audio_data">
      <template #headerCell="{ column }">
        <template v-if="column.key === 'name'">
          <span> Name </span>
        </template>
      </template>

      <template #bodyCell="{ index, column, record }">
        <template v-if="column.key === 'index'">
          <div>
            {{ index + 1 }}
          </div>
        </template>
        <template v-if="column.key === 'name'">
          <a>
            {{ limitTextLength(record.name, 20) }}
          </a>
        </template>
        <template v-if="column.key === 'content'">
          {{ limitTextLength(record.content, 300) }}
        </template>
      </template>
    </Table>
  </div>
</template>

<script>
import axios from "axios";
import { Table } from "ant-design-vue";
export default {
  components: { Table },
  data() {
    return {
      selectedFile: null,
      audio_data: [],
      columns: [
        {
          name: "Index",
          dataIndex: "index",
          key: "index",
        },
        {
          name: "Name",
          dataIndex: "name",
          key: "name",
        },
        {
          title: "Content",
          dataIndex: "content",
          key: "content",
        },
        {
          title: "Category",
          dataIndex: "category",
          key: "category",
        },
        {
          title: "Similarity",
          dataIndex: "similarity",
          key: "similarity",
        },
      ],
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async submitFile() {
      const formData = new FormData();
      formData.append("file", this.selectedFile);

      axios.post("http://localhost:5000/file/upload", formData)
      .then((res) => {
          this.audio_data = res.data;
        });
    },
    limitTextLength(text, length) {
      if (text && text.length >= length) {
        return `${text.slice(0, length)}...`;
      }
      return text;
    },
  },
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.file-input {
  margin-bottom: 10px;
}

.upload-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}

.upload-button:hover {
  background-color: #45a049;
}
</style>