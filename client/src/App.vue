<script setup lang="ts">
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Dropdown from "primevue/dropdown";
import MultiSelect from "primevue/multiselect"
import Button from "primevue/button";
import TabPanel from "primevue/tabpanel";
import TabView from "primevue/tabview";
import {computed, onMounted, ref} from "vue";

let outputs = ref(new Array<{ generator: string, values: string }>)
let chosenFiles = ref([]);
let fileNames = ref([]);
let depthCreate = ref(3);
let depthGen = ref(3);
let amount = ref(100);
let lmin = ref(0);
let lmax = ref(10);
let newGeneratorName = ref("");

let generatorNames = ref(new Array<string>());
let chosenGenerator = ref("");

onMounted(async() => {
  await loadFileNames();
  await loadGeneratorNames();
});

async function loadFileNames(){
  const response = await fetch("http://127.0.0.1:5000/get_inputfiles", {});
  fileNames.value = await response.json();
}

async function loadGeneratorNames(){
  const response = await fetch("http://127.0.0.1:5000/get_generators", {});
  const data = await response.json();
  generatorNames.value = data;
}

async function createGenerator(){
  let params = { name: newGeneratorName.value, depth: depthCreate.value, filenames: chosenFiles.value, optional_values: "", lmin: lmin.value, lmax: lmax.value};
  const response = await fetch("http://127.0.0.1:5000/create_generator", {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(params)
  });
  const data: string = await response.json();
  generatorNames.value.push(data);

  await loadGeneratorNames();
}

async function removeGenerator(name: string){
  let params = { name: name };
  const response = await fetch("http://127.0.0.1:5000/remove_generator", {
    method: 'DELETE',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(params)
  });
  const data: string = await response.json();
  await loadGeneratorNames();

}

async function generateNames() {
  let params = { generator_name: chosenGenerator.value,amount: amount.value, depth: depthGen.value, lmin: lmin.value, lmax: lmax.value};
  const response = await fetch("http://127.0.0.1:5000/generate_names", {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(params)
  });
  const data: [] = await response.json();
  outputs.value.push({generator: chosenGenerator.value, values: data.join("")});
}

const _gennames = computed(() => {
  return generatorNames.value;
})

const _outputs= computed(() => {
  return outputs.value
})

function downloadResult (index:number) {
  console.log("index " + index);
  const blob = new Blob([_outputs.value[index].values], { type: 'plain/text' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = _outputs.value[index].generator+".txt"
  link.click()
  URL.revokeObjectURL(link.href)
}
</script>

<template>
  <div class="container">
    <section class="header">
      <h1>Markov-Namensgenerator v.1.0</h1>
    </section>
    <section class="control">
      <div class="column">
        <div class="control-fields">
          <span>
            <label>Eingabedateien:</label>
            <MultiSelect :options="fileNames" v-model="chosenFiles" placeholder="Bitte wählen Sie" >
              <template #option="slotProps">
                {{ slotProps.option.split("/").slice(-1)[0] }}
              </template>
            </MultiSelect>
          </span>
          <span>
            <label>Tiefe:</label>
            <InputNumber v-model="depthCreate" />
          </span>
          <span>
            <label>Generator-Name:</label>
            <InputText v-model="newGeneratorName" />
          </span>
        </div>
        <Button @click.prevent="createGenerator()" label="Generator erstellen" />
      </div>
      <div class="column">
        <div class="control-fields">
          <span>
            <label>Generatorauswahl:</label>
            <Dropdown :options="_gennames" v-model="chosenGenerator" placeholder="Bitte wählen Sie">
              <template #option="slotProps">
                <label>{{slotProps.option}}</label>
                <button icon="pi pi-plus" @click="removeGenerator(slotProps.option)"/>
              </template>
            </Dropdown>
          </span>
          <span>
            <label>Tiefe:</label>
            <InputNumber v-model="depthGen" />
          </span>
          <span>
            <label>Mindestlänge:</label>
            <InputNumber v-model="lmin" />
          </span>
          <span>
            <label>Maximallänge:</label>
            <InputNumber v-model="lmax" />
          </span>
          <span>
            <label>Anzahl:</label>
            <InputNumber v-model="amount" />
          </span>
        </div>
        <Button @click="generateNames()" label="Namen generieren" />
      </div>
    </section>
    <section class="hline">
      <div>{{ chosenFiles.map((file) => file.split("/").slice(-1)[0]).join(", ") }}</div>
    </section>
    <section class="output">
      <TabView>
        <TabPanel v-for="(output,index) in _outputs" :key="index" :header="output.generator">
          <Button label="Download" @click.prevent="downloadResult(index)" style="padding-right: 1em"/>
          {{output.values}}
        </TabPanel>
      </TabView>
    </section>
  </div>
</template>

<style scoped>

h1 {
  font-size: 30px;
  font-weight: bold;
}
.container {
  display: block;
  min-width: 70vw;
  max-width: 70vw;
  height: 100vh;

}

.header {
  display: flex;
  padding-top: 5em;
  padding-bottom: 4em;
}

.control {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.column {
  height: 40vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.control-fields {
  width: 30vw;
}

.control-fields span {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 0.2em;
}

::v-deep(.p-inputtext){
  min-width: 10em;
  max-width: 10em;
  min-height: 2em;
  max-height: 2em;
  background-color: white;
  color: black;
}

::v-deep(.p-dropdown){
  min-width: 10em;
  max-width: 10em;
  min-height: 2em;
  max-height: 2em;
  background-color: white;
  color: black;
}

::v-deep(.p-multiselect){
  min-width: 10em;
  max-width: 10em;
  min-height: 2em;
  max-height: 2em;
  background-color: white;
  color: black;
}



.hline {
  margin-top: 6em;
}

.output {
  display: flex;
  padding: 0.5em;
  width: inherit;
  border: 1px solid black;
}

</style>
