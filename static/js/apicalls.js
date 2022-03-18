async function getLights() {
    let url = 'https://zmood.local:5000/api/lights';
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function setLightsOn() {
    var x = document.getElementById("myLights").selectedIndex;
    var id = document.getElementsByTagName("option")[x].value;
    let url = 'https://zmood.local:5000/api/lights/on/' + id;
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function setLightsOff() {
    var x = document.getElementById("myLights").selectedIndex;
    var id = document.getElementsByTagName("option")[x].value;
    let url = 'https://zmood.local:5000/api/lights/off/' + id;
    try {
        let res = await fetch(url);
        return await res.json();
    } catch (error) {
        console.log(error);
    }
}

async function renderLights() {
    let lights = await getLights();
    let html = '';
    lights.map(light => {
        let htmlSegment = `<option value="${light.id}">${light.name}</option>`;
        if (light.state == 1) {
            htmlSegment = `<option value="${light.id}" selected>${light.name}</option>`;
        }
        html += htmlSegment;
    });

    let container = document.querySelector('.form-select');
    container.innerHTML = html;
}

renderLights();
