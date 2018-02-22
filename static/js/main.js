let compareButton = document.getElementById("compare-button");

function escapeHtml(text) {
	let map = {
		'&': '&amp;',
		'<': '&lt;',
		'>': '&gt;',
		'"': '&quot;',
		"'": '&#039;',
		'\n': '<br>\n'
	};

	return text.replace(/[&<>"'\n]/g, function (m) {
		return map[m];
	});
}

compareButton.addEventListener("click", function () {
	let text1 = escapeHtml(document.getElementById("doc1_text").value),
		text2 = escapeHtml(document.getElementById("doc2_text").value),
		config = {
			deleted_element: document.getElementById("deleted_element").value,
			inserted_element: document.getElementById("inserted_element").value,
			modified_class: document.getElementById("modified_class").value,
			deleted_class: document.getElementById("deleted_class").value,
			inserted_class: document.getElementById("inserted_class").value,
		},
		resultField = document.getElementById("compare-result");

	console.log(text1, text2);
	axios.post('/api/v1.0/diff', {
		doc1: text1,
		doc2: text2,
		config: config
	})
		.then(function (response) {
			resultField.innerHTML = "<p><strong>Result:</strong></p>" + response.data.result
		})
		.catch(function (error) {
			resultField.innerHTML = "<p><strong>Error:</strong></p>" + error;
			console.error(error);
		});
});

function readTextFile(file_input_id) {
	// obtain input element through DOM

	const file = document.getElementById(file_input_id).files[0];
	if (file) {
		getAsText(file, file_input_id);
	}
}

function getAsText(readFile, file_input_id) {

	let reader = new FileReader();

	reader.readAsText(readFile, "UTF-8");

	reader.onload = function (evt) {
		loaded(evt, file_input_id)
	};
	reader.onerror = errorHandler;
}

function loaded(evt, file_input_id, text_id_postfix = "_text") {
	document.getElementById(file_input_id + text_id_postfix).value = evt.target.result
}

function errorHandler(evt) {
	if (evt.target.error.name === "NotReadableError") {
		console.error("The file could not be read")
	}
}

function multipleReadTextFile(input_id_list) {
	input_id_list.forEach(function (input_id) {
		document.getElementById(input_id).addEventListener('change', function (e) {
			readTextFile(input_id);
		}, false);
	});
}


$(document).ready(function () {
	multipleReadTextFile(["doc1", "doc2"])
});