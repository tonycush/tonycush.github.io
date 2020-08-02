document.write('\
<ul class="nav nav-tabs" id="myTab" role="tablist">\
    <li class="nav-item">\
        <a class="nav-link active" id="overviews-tab" data-toggle="tab" href="#overviews" role="tab" aria-controls="overviews" aria-selected="true">Overviews</a>\
    </li>\
    <li class="nav-item">\
        <a class="nav-link" id="details-tab" data-toggle="tab" href="#details" role="tab" aria-controls="details" aria-selected="false">Details</a>\
    </li>\
    <li class="nav-item">\
        <a class="nav-link" id="people-tab" data-toggle="tab" href="#people" role="tab" aria-controls="people" aria-selected="false">People</a>\
    </li>\
    <li class="nav-item">\
        <a class="nav-link" id="accounts-tab" data-toggle="tab" href="#accounts" role="tab" aria-controls="accounts" aria-selected="false">Accounts??</a>\
    </li>\
    <li class="nav-item">\
        <a class="nav-link" id="placeholder1-tab" data-toggle="tab" href="#placeholder1" role="tab" aria-controls="placeholder1" aria-selected="false">Place holder</a>\
    </li>\
</ul>\
<div class="tab-content" id="myTabContent">\
    <div class="tab-pane fade show active" id="overviews" role="tabpanel" aria-labelledby="overviews-tab">\
        <div id="ch_overview" class="card abd"></div>\
        <div id="cb_intro" class="abd"></div>\
        <div id="cb_overview" class="card abd"></div>\
    </div>\
    <div class="tab-pane fade" id="details" role="tabpanel" aria-labelledby="details-tab">\
        <div id="cb_details"></div>\
    </div>\
    <div class="tab-pane fade" id="people" role="tabpanel" aria-labelledby="people-tab">\
        <div id="ch_people"></div>\
    </div>\
    <div class="tab-pane fade" id="accounts" role="tabpanel" aria-labelledby="accounts-tab">\
        Accounty countametre\
        <div id="accounts_info" class="comp_output">\
        <div id="accounts_filed">All Listed</div>\
        <div id="accounts_turked"><br><h4>Turker jobs</h4></div>\
        <div id="accounts_ixbrl"><br><h4>iXBRL details</h4></div>\
        <br>\
        <div id="accounts_output"><br><h4>Output</h4></div>\
        </div>\
    </div>\
    <div class="tab-pane fade" id="placeholder1" role="tabpanel" aria-labelledby="placeholder1-tab">Hold my place!</div>\
</div>\
');