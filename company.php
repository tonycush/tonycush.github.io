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

    <style>
        .comp_output {
            border: solid;
            margin-top: 1em;
        }

        #newDiv {
            text-decoration: underline;
        }
    </style>
</head>

<body>
    <h1>Company Demo</h1>
    <h3>Company INFO</h3>
    <?php
    $temp_company = $_GET['name'];
    echo "<h3>" . $temp_company . "</h3>";
    ?>
    <div id="sample" style="background-color: beige;"></div>
    <div id="details"></div>

    <!-- Optional JavaScript -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>

</body>
<script type="text/javascript">
    fetch("crunchbase_info_sample.json")
        .then(function(response) {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then(function(mydata) {
            console.log("RIGHT - I only want this FILE")
            var this_company_name = '<?php $this_company = $_GET['name'];
                                        echo $this_company ?>'

            console.log(this_company_name);
            console.log(mydata);
            var this_company_pos = mydata.findIndex((item) => item.name === this_company_name);
            console.log(mydata[this_company_pos])
            var ths_comp_out = (JSON.stringify(mydata[this_company_pos]));

            var new_section = document.createElement('div');

            new_section.className = "comp_output";
            new_section.id = "sect_id";
            new_section.innerHTML = "howzatt??";
            document.getElementById("sample").appendChild(new_section);

            var sec_keys = Object.keys(mydata[this_company_pos].sections[0]);
            for (var i = 0; i < mydata[this_company_pos].sections.length; i++) {
                var ori_name = mydata[this_company_pos].sections[i].name;
                var temp_name = ori_name.replace('<!---->', '')
                var updated = temp_name.trim();     
                if (updated != "null") {
                    new_section = document.createElement('div');
                    new_section.className = "comp_output";
                    new_section.id = updated;
                    new_section.innerHTML = '<strong>' + updated + '</strong>';
                    document.getElementById("details").appendChild(new_section);

                    for (var j = 0; j < sec_keys.length; j++) {
                        entry = sec_keys[j];
                        entry_type = typeof(mydata[this_company_pos].sections[i][entry]);
                        entry_length = mydata[this_company_pos].sections[i][entry].length;
                        if (entry_type == 'object' && entry_length > 0) {
                            switch (entry) {
                                case 'table':
                                    console.log("Aye, thon's a table")
                                    break;

                                case 'imageCard':
                                    //console.log("--- -- ---- -- - ---");
                                    //console.log(updated + " : " + entry + " = " + entry_length);
                                    image_count = (mydata[this_company_pos].sections[i][entry][0]["rows"].length)
                                    image_keys = Object.keys(mydata[this_company_pos].sections[i][entry][0]["rows"][0]);
                                    image_table = document.createElement('table');
                                    image_table.className= "table table-striped";
                                    image_table.innerHTML = "<strong><thead><tr><th>logo</th><th>Name</th><th>Info</th></tr></thead></strong>";
                                    image_body = "<tbody>"
                                    for (var k = 0 ; k<image_count; k++){
                                        
                                        image_body += "<tr>";
                                        for (var l = 0; l < image_keys.length; l++){
                                            this_image_key = image_keys[l]
                                            image_detail = mydata[this_company_pos].sections[i][entry][0]["rows"][k][this_image_key];                                            
                                            image_body += "<td>"+image_detail+"</td>";
                                        }
                                        
                                        image_body += "</tr>";
                                    }
                                    image_body += "</tbody>";
                                    image_table.innerHTML += image_body;
                                    document.getElementById(updated).appendChild(image_table);
                                    break;
                                default:
                                    for (var k = 0; k < entry_length; k++) {
                                        this_detail_keys = Object.keys(mydata[this_company_pos].sections[i][entry][k]);
                                        this_detail_values = Object.values(mydata[this_company_pos].sections[i][entry][k]);
                                        section_info = document.createElement('p');
                                        section_info.innerHTML = this_detail_keys + " ::: " + this_detail_values;

                                        document.getElementById(updated).appendChild(section_info);

                                    }
                            }

                            //console.log("--- -- ---- -- - ---");
                        }
                    }

                }
            }

        })
</script>


</html>