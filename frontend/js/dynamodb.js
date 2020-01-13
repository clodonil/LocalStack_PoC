AWS.config.update({
  region: "us-east-1",
  endpoint: 'http://localhost:4569',
});


var dynamodb = new AWS.DynamoDB();
var docClient = new AWS.DynamoDB.DocumentClient();

$(document).ready(function() {
    $('#submit-btn').on('click', function() {
      alert("ersre");
    });
  });


function createItem() {
    var params = {
        TableName :"produtos",
        Item:{
            "email": "clodonil@nisled.org",
            "nome_produto": "Bola de Futebol",
            "detail":{
                "status": "true",
                "preco_compra": "90.0",
                "min_preco" : {"preco":"0"},
                "max_preco" : {"preco":"0"}
            }
        }
    };
    docClient.put(params, function(err, data) {
        if (err) {
            document.getElementById('textarea').innerHTML = "Unable to add item: " + "\n" + JSON.stringify(err, undefined, 2);
        } else {
            document.getElementById('textarea').innerHTML = "PutItem succeeded: " + "\n" + JSON.stringify(data, undefined, 2);
        }
    });
}
