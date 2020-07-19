<html>

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/css/bootstrap.min.css" integrity="sha384-r4NyP46KrjDleawBgD5tp8Y7UzmLA05oM1iAEQ17CSuDqnUK2+k9luXQOfXJCJ4I" crossorigin="anonymous">
    <link href="https://unpkg.com/tabulator-tables@4.7.2/dist/css/tabulator.min.css" rel="stylesheet">
    <link href="/dist/css/bootstrap/tabulator_bootstrap4.min.css" rel="stylesheet">
    <script type="text/javascript" src="https://unpkg.com/tabulator-tables@4.7.2/dist/js/tabulator.min.js"></script>
</head>

<body>
    <h1>Company Demo</h1>
    <ul id="sample-info"></ul> 
    <div id="demo"></div>
    <div id="json-table"></div>
    <!-- Optional JavaScript -->
   <!-- Popper.js first, then Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.0.0-alpha1/js/bootstrap.min.js" integrity="sha384-oesi62hOLfzrys4LxRF63OJCXdXDipiYWBnvTl9Y9/TRlw5xlKIEHpNyvvDShgf/" crossorigin="anonymous"></script>
  
</body>

<script type="text/javascript">

    var myList = document.querySelector('#sample-info');
    fetch("crunchbase_info_sample.json")
        .then(function (response) {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then(function (json) {
            console.log("This is the sample JSON file...")
            console.log(json)


            //console.log("Listing the sample JSON file...")
            for (var i = 0; i < json.length; i++) {

            //for (var i = 0; i < 1; i++) {

                var headers = Object.keys(json[i])
                //console.log(headers);
                //console.log(headers.length);
                var listItem = document.createElement('li');
                listItem.innerHTML = '<strong>' + json[i].name + '</strong>';
                listItem.innerHTML += ' : '+json[i].company_number;
                listItem.innerHTML += ' can be found in ' + json[i].location + '.';
                listItem.innerHTML += '<ul><li>Basically : '+json[i].basicInfo+'</li><li>Desc : '+json[i].description+'</li></ul>';
                myList.appendChild(listItem);


                sec_len = json[i].sections.length;
            }

            //console.log("\nHoping to access the keys...")
            for (x in json) {

                //console.log(Object.values(x));
                document.getElementById("demo").innerHTML += json[x];
            }
        })

        .catch(function (error) {
            var p = document.createElement('p');
            p.appendChild(
                document.createTextNode('Error: ' + error.message)
            );
            document.body.insertBefore(p, myList);
        });


</script>

<script type="text/javascript">

    fetch("crunchbase_info_sample.json")
        .then(function (response) {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then(function (mydata) {
            //create Tabulator on DOM element with id "example-table"
            var table = new Tabulator("#json-table", {
                index: "index",
                dataTree: true,
                height: 205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
                data: mydata, //assign data to table
                layout: "fitColumns", //fit columns to width of table (optional)
                columns: [

                    //Define Table Columns
                    //{ formatter: "rownum", hozAlign: "center", width: 40 },

                    //{ title: "Numero", field: "index" },
                    { title: "Name", field: "name" },
                    { title: "Basic", field: "basicInfo" },
                    {
                        title: "Founders", field: "fake2", formatter: function (row) {    
                            //console.log(row);
                            var x = row.getData();                            
                            //console.log(x);
                            
                            var y = (x["basicInfo"]);
                            //console.log(y);

                            var pos = x.sections.indexOf(" Overview <!---->");
                            //console.log(pos);

                            var len = x.sections.length;
                            /*
                            for (var a = 0; a<len; a++){
                                temp = x.sections[a].name;
                                if (temp != "null"){
                                    console.log(temp);
                                }
                            };

                            */
                            var namo = x.sections.findIndex((item) => item.name === " Overview <!---->" );
                            //console.log(namo)
                            
                            console.log(x.sections[namo].name)    
                            console.log("---- ---  - - - ----  ");                          
                            
                            ov_len = x.sections[namo].data.length
                            console.log(ov_len)
                            for (var a = 0; a<ov_len; a++){
                                temp = x.sections[namo].data[a];
                                key_temp = Object.keys(temp)
                                if (key_temp == "Founders "){
                                    console.log(a);
                                }
                            };
                            
                            //console.log(Object.values(x.sections[namo].data))
                            console.log("**** *** ** ** *** ");
                            var fondo = x.sections[namo].data.findIndex(item => (Object.keys(item))[0] === "Founders " );
                            console.log(fondo)
                            
                            console.log("**** *** ** ** *** ");
                            console.log(x.sections[namo].data[fondo]);
                            z= (x["sections"][0].name);
                            //console.log(z);
                            f = (x.sections[namo].data[fondo]);
                            g = Object.values(f);
                            console.log(g);
                            return g[0];
                        },
                    },{
                        title: "Industries", field: "fake3", formatter: function (row) { 
                            var x = row.getData();  
                            var pos = x.sections.indexOf(" Overview <!---->");
                            var len = x.sections.length;
                            var namo = x.sections.findIndex((item) => item.name === " Overview <!---->" );                            
                            ov_len = x.sections[namo].data.length
                            var fondo = x.sections[namo].data.findIndex(item => (Object.keys(item))[0] === "Industries " );
                            z= (x["sections"][0].name);
                            f = (x.sections[namo].data[fondo]);
                            g = Object.values(f);
                            return g[0];
                        },
                    },
                ],
                rowClick: function (e, row) { //trigger an alert message when the row is clicked
                    alert("Row " + row.getData().id + " Clicked!!!!");
                },
            });

        })

        .catch(function (error) {
            var p = document.createElement('p');
            p.appendChild(
                document.createTextNode('Error: ' + error.message)
            );
            document.body.insertBefore(p, myList);
        });




</script>

</html>