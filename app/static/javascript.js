(function (win,doc){

	'use strict';
	// Verifica se o usuario deseja deletar o registro
	if (doc.querySelector('.btnDel')){
		let btnDel = doc.querySelectorAll('.btnDel');
		for (let i=0; i < btnDel.length; i++) {
			btnDel[i].addEventListener('click', function(event){
				if(confirm('Deseja apagar o registro?')){
					return true;
				}else{
					event.preventDefault();
				}

			});
		}
	}
	

	// Ajax para o form de cadastro

	if (doc.querySelector('#form')){
		let form=doc.querySelector('#form');

		function sendForm(event)
			event.preventDefault();
			let data = new  FormData(form);
			let ajax = new  XMLHttpRequest();
			let token = doc.querySelectorAll('input')[0].value;
			
			ajax.open('POST', form.action);
			ajax.setRequestHeader('X-CSRF-TOKEN',token);
			
			ajax.onreadystatechange = function(){
				if(ajax.status == 200 && ajax.readyState == 4){
					let result = doc.querySelector('#result');
					result.innerHTML = 'Operação realizada com Sucesso!!!'
					result.classList.add('alert');
					result.classList.add('alert-success');	
				}
			}
			ajax.send(data);
			form.reset();
		}
		form.addEventListener('submit'.sendForm,false)
	} 


	if (doc.querySelector('#cep')){
		function buscaCep() { 
			let inputCep = document.querySelector('input\[#cep\]'); 
			console.log(inputCep);
			let cep = inputCep.value.replace('-', '');
			let url = 'http://viacep.com.br/ws/' + cep + '/json'; 
			let xhr = new XMLHttpRequest(); xhr.open('GET', url, true); 
			xhr.onreadystatechange = function() { 
			if (xhr.readyState == 4) { 
			if (xhr.status = 200) preencheCampos(JSON.parse(xhr.responseText)); } } 
			xhr.send(); 
		}
	}
	
	function preencheCampos(json) { 
		document.querySelector('input[name=endereco]').value = json.logradouro;
		document.querySelector('input[name=bairro]').value = json.bairro; 
		document.querySelector('input[name=endcompl]').value = json.complemento;
		document.querySelector('input[name=cidade]').value = json.localidade; 
		document.querySelector('input[name=uf]').value = json.uf; 
	}

}) (window,document);
