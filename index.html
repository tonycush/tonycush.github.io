<html>

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
        integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    <link href="https://unpkg.com/tabulator-tables@4.7.2/dist/css/tabulator.min.css" rel="stylesheet">
    <link href="/dist/css/bootstrap/tabulator_bootstrap4.min.css" rel="stylesheet">
    <script type="text/javascript" src="https://unpkg.com/tabulator-tables@4.7.2/dist/js/tabulator.min.js"></script>
</head>

<body>
    <h1>Company Demo</h1>

    <div id="json-table"></div>
    <!-- Optional JavaScript -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
        integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
        crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"
        integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
        crossorigin="anonymous"></script>
</body>

<script type="text/javascript">

    fetch("crunchbase_info_tidy.json")
        .then(function (response) {
            if (!response.ok) {
                throw new Error("HTTP error, status = " + response.status);
            }
            return response.json();
        })
        .then(function (mydata) {
            //create Tabulator on DOM element with id "json-table"
            var table = new Tabulator("#json-table", {
                index: "index",
                dataTree: true,
                //height: 205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
                data: mydata, //assign data to table
                layout: "fitColumns", //fit columns to width of table (optional)
                columns: [
                    //Define Table Columns
                    {
                        title: "Name", field: "name", sorter: "string", headerSortTristate: true, formatter: "link", formatterParams: {
                            url: function (cell) {
                                var linkage = "company.html?" + cell.getData().name;
                                return linkage;
                            },
                            target: "_blank",
                        }
                    },
                    { title: "Basic", field: "basicInfo", sorter: "string" },
                    {
                        title: "Industries", field: "industries", sorter: "string", formatter: function (row) {
                            var x = row.getData();
                            var section_len = x.sections.length;
                            var overview_pos = x.sections.findIndex((item) => item.name === "Overview");
                            var overview_len = x.sections[overview_pos].data.length
                            var info_pos = x.sections[overview_pos].data.findIndex(item => (Object.keys(item))[0] === "Industries ");
                            if (info_pos == -1) {
                                return "NA"
                            } else {
                                info_array = (x.sections[overview_pos].data[info_pos]);
                                info_vals = Object.values(info_array);
                                var details = "";
                                for (var i = 0; i < info_vals.length; i++) {
                                    details += info_vals[i] + ","
                                }
                                details = details.slice(0, -1);
                                return details;
                            }

                        },
                    },
                    {
                        title: "Foundry", field: "founders", sorter: "string", formatter: function (row) {
                            var x = row.getData();
                            var section_len = x.sections.length;
                            var overview_pos = x.sections.findIndex((item) => item.name === "Overview");
                            var overview_len = x.sections[overview_pos].data.length
                            var info_pos = x.sections[overview_pos].data.findIndex(item => (Object.keys(item))[0] === "Founders ");
                            if (info_pos == -1) {
                                return "NA"
                            } else {
                                info_array = (x.sections[overview_pos].data[info_pos]);
                                info_vals = Object.values(info_array);
                                var details = "";
                                for (var i = 0; i < info_vals.length; i++) {
                                    details += info_vals[i] + ","
                                }
                                details = details.slice(0, -1);
                                return details;
                            }
                        },
                    },
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