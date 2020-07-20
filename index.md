<html>

    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
        <link href="https://unpkg.com/tabulator-tables@4.7.2/dist/css/tabulator.min.css" rel="stylesheet">
        <link href="/dist/css/bootstrap/tabulator_bootstrap4.min.css" rel="stylesheet">
        <script type="text/javascript" src="https://unpkg.com/tabulator-tables@4.7.2/dist/js/tabulator.min.js"></script>
    </head>

<body>
    <h1>Company Demo</h1>
    <div style="background-color: azure">

        <ul>
            <li>Just some sample info</li>
        </ul>
    </div>

    <ul id="demo-info" style ="background-color: beige;"></ul>

    <div id="example-table"></div>

    <div id="demo"></div>

    <button type="button" class="btn">Basic</button>
    
    <button type="button" class="btn btn-success">Success</button>

    <div id="json-table"></div>

    <!-- Optional JavaScript -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
  
</body>

<script type="text/javascript">

    var myList = document.querySelector('#demo-info');
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

                /*
                var headers = Object.keys(json[i])
                //console.log(headers);
                //console.log(headers.length);
                var listItem = document.createElement('li');
                listItem.innerHTML = '<strong>' + json[i].index + '</strong>';
                listItem.innerHTML += ' can be found in ' + json[i].name + '.';
                listItem.innerHTML += ' Cost: <strong>£' + json[i].basicInfo + '</strong>';
                myList.appendChild(listItem);
                */

                sec_len = json[i].sections.length;
                //console.log(sec_len);
                /*
                //This will print the name of each section
                for (var k = 0; k< sec_len; k++){
                    console.log(json[i].sections[k].name)
                }

                */

                /*
                //Printing out the industries
                for (var k = 0; k < sec_len; k++) {
                    if (json[i].sections[k].name == " Overview <!---->") {
                        console.log("ALERT ******")
                        overv_len = json[i].sections[k].data.length;
                        console.log(overv_len);

                        for (var l = 0; l < overv_len; l++) {
                            //console.log(Object.keys(json[i].sections[k].data[l]))

                            if (Object.keys(json[i].sections[k].data[l]) == "Industries ") {
                                console.log(Object.values(json[i].sections[k].data[l]))
                            }
                            //console.log(json[i].sections[k].data[l]);
                        }
                    }
                    //console.log(json[i].sections[k].name)
                }
                */

                //console.log(json[i].sections.length);
                //var subheaders = Object.keys(json[i].sections)
                //console.log(subheaders)

                /*
                for(var k = 0; k < json[i].sections.length; k++ ){
                    //console.log(Object.keys(json[i].sections[k]))
                    console.log(json[i].sections[k].name)
                    console.log(Object.values(json[i].sections[k].data))
                    console.log(json[i].sections[k].fields)
                    console.log(json[i].sections[k].imageCard)
                    console.log(json[i].sections[k].table)
                }
                */
                /*
                for (var j = 0; j <headers.length; j++ ){
                    if (headers[j] =="section"){
                        console.log(Object.keys(headers[j]));
                    }
                    //console.log(headers[j]);
                }
                */
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
            //define some sample data
            //var jtabledata = mydata;
            //console.log(jtabledata)
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
                    { title: "Name", field: "name" ,sorter:"string", headerSortTristate:true,formatter:"link", formatterParams:{
                        
                        url:function(cell){
                            console.log("** LINKAGE ****");
                            var linkage = "company.html?"+cell.getData().name;
                            console.log(linkage);
                            return linkage ;
                        },
                        target:"_blank",
                    }},
                    { title: "Basic", field: "basicInfo" ,sorter:"string"},
                    {
                        title: "Founders", field: "founders",sorter:"string", headerSort:false, formatter: function (row) {    
                            //console.log(row);
                            var x = row.getData();                            
                            //console.log(x);
                            
                            var y = (x["basicInfo"]);
                            //console.log(y);

                            var pos = x.sections.indexOf(" Overview <!---->");
                            //console.log(pos);

                            var len = x.sections.length;
                            //console.log(len);
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
                            console.log(typeof(g[0]));
                            return g[0];
                        },
                    },{
                        title: "Industries",field:"industries",sorter:"string", formatter: function (row) { 
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
                    /*
                    {
                        title: "Industries", field: "fake", formatter: function (value, data, cell, row, options, rownum) {
                            //console.log("JTABLE JSON ******");
                            var this_ind;
                            //console.log(rownum);
                            for (var i = 0; i < mydata.length; i++) {
                                //console.log(Object.keys(mydata[i]))
                                var sec_len = mydata[i].sections.length;
                                //console.log(sec_len);
                                for (var k = 0; k < sec_len; k++) {
                                    if (mydata[i].sections[k].name == " Overview <!---->") {
                                        //console.log("OVERVIEW ALERT ******")
                                        overv_len = mydata[i].sections[k].data.length;
                                        //console.log(overv_len);

                                        for (var l = 0; l < overv_len; l++) {
                                            //console.log(Object.keys(json[i].sections[k].data[l]))

                                            if (Object.keys(mydata[i].sections[k].data[l]) == "Industries ") {
                                                //console.log(Object.values(json[i].sections[k].data[l]));
                                                //this_ind = JSON.stringify(Object.values(mydata[i].sections[k].data[l]));
                                                this_ind = (Object.values(mydata[i].sections[k].data[l]));

                                            }
                                            //console.log(json[i].sections[k].data[l]);
                                        }
                                    }
                                    //console.log(json[i].sections[k].name)
                                }
                            }

                            var i = 0;

                            //console.log(jtabledata.name);
                            //console.log(Object.values(jtabledata.sections))
                            console.log(this_ind);

                            return (this_ind[0]);
                        }
                    }, */
                ],
                rowClick: function (e, row) { //trigger an alert message when the row is clicked
                    console.log("Row " + row.getData().name + " Clicked!!!!");
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