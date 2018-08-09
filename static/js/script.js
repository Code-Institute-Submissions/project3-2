$('#taskdesc').on('change', function() {
    if(this.value == "Buy" || this.value == "Keep" || this.value == "Gift Donate")
        $("#for_return").hide();
    else
        $("#for_return").show();
}) 