
    fetch("my_files/crunchbase_info_tidy.json")
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
            pagination: "local",
            paginationSize: 20,
            paginationSizeSelector: [10, 20, 30, 40, 50],
            //height: 205, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
            data: mydata, //assign data to table
            layout: "fitColumns", //fit columns to width of table (optional)
            columns: [
                //Define Table Columns
                {
                    title: "Name", field: "name", sorter: "string", headerSortTristate: true, formatter: "link", formatterParams: {
                        url: function (cell) {
                            //console.log(cell.getData());
                            //var linkage = "company.html?" + cell.getData().name;
                            var linkage = "company.html?" + cell.getData().company_number;
                            return linkage;
                        },
                        target: "_blank",
                    }
                },
                { title: "Basic", field: "basicInfo", sorter: "string", headerSortTristate: true },
                {
                    title: "iXBRL", field: "any_iXBRL", sorter: "string", formatter: function (row) {
                        var x = row.getData(data)
                        console.log(x)
                        y = "WHO KNOWS?"
                        return y
                    }
                },
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