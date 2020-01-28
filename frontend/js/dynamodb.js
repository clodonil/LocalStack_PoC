AWS.config.update({
    region: "us-east-1",
    endpoint: 'http://localhost:4569',
    accessKeyId: "fakeMyKeyId",
    secretAccessKey: "fakeSecretAccessKey"
  });
  
  
  var dynamodb = new AWS.DynamoDB();
  var docClient = new AWS.DynamoDB.DocumentClient();
  
  
 
  function createItem() {
   
      var email = document.getElementById('email').value;
      var produto = document.getElementById('produto').value;
      var preco = document.getElementById('preco').value;

      var params = {
          TableName :"produtos",
          Item:{
              "email": email,
              "produto": produto,
              "details":{
                  "status" : "true",
                  "preco_compra" : preco
              }
          }
      };
      docClient.put(params, function(err, data) {
          if (err) {
            M.toast({html: 'Não foi possível registrar o seu pedido.'});
          } else {
              document.getElementById('email').value = "";
              document.getElementById('produto').value = "";
              document.getElementById('preco').value = "";              
              M.toast({html: 'Produto cadastro com sucesso!!!'})
          }
      });
  

  }
  
  
  
  