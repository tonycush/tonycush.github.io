console.log("Well hopefully this is in the right place")

document.write('\
<ul class="nav nav-tabs" id="myTab" role="tablist">\
    <li class="nav-item">\
        <a class="nav-link active" id="overviews-tab" data-toggle="tab" href="#overviews" role="tab" aria-controls="overviews" aria-selected="true">Overviews</a>\
    </li>\
    <li class="nav-item">\
        <a class="nav-link" id="profile-tab" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false">Profile</a>\
    </li>\
    <li class="nav-item">\
        <a class="nav-link" id="accounts-tab" data-toggle="tab" href="#accounts" role="tab" aria-controls="accounts" aria-selected="false">Contact</a>\
    </li>\
    <li class="nav-item">\
        <a class="nav-link" id="placeholder1-tab" data-toggle="tab" href="#placeholder1" role="tab" aria-controls="placeholder1" aria-selected="false">Place holder</a>\
    </li>\
</ul>\
<div class="tab-content" id="myTabContent">\
    <div class="tab-pane fade show active" id="overviews" role="tabpanel" aria-labelledby="overviews-tab">Hey, check out my overviews</div>\
    <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">Let\'s dig in</div>\
    <div class="tab-pane fade" id="accounts" role="tabpanel" aria-labelledby="accounts-tab">Accounty countametre</div>\
    <div class="tab-pane fade" id="placeholder1" role="tabpanel" aria-labelledby="placeholder1-tab">Hold my place!</div>\
</div>\
');