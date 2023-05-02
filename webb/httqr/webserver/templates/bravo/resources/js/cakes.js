var viewModel = {
    cakes: ko.observable()
};

ko.applyBindings(viewModel, $('#cakeTable').get(0));

async function retrieveJson(url, params) {
    let options = {
        method: 'POST',
        body: JSON.stringify(params),
        headers: {"Content-Type": "application/json"}
    };
    return fetch(url, options).then(response => response.json());
}

function setCakeView(data) {
    viewModel.cakes(data);
}

async function updateCakeView() {
    retrieveJson('/cakeview', {'include_flag':false}).then(data => setCakeView(data));
}

function initCakePage() {
    updateCakeView();
}

initCakePage();

