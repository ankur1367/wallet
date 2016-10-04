$("a").focus(
    function(){
        this.blur();
    });

var newWalletForm =' <div id="add-new-wallet-form" class="col-md-2 wallet-block wallet-frame disabled"> <form class="form-horizontal" role="form"> <div id="name-group" class="form-group"> <input id="new-wallet-name" type="text" class="form-control input-sm" placeholder="Wallet name"> </div> <hr> <div id="type-group" class="form-group"> <input id="new-wallet-type" type="text" class=" form-control input-sm" placeholder="Currency (USD,EUR,etc.)"> </div> <hr> <div id="sum-group" class="form-group"> <input id="new-wallet-sum" type="text" class="form-control input-sm" placeholder="Available (5000)"> </div> <hr> <p><a id="add-new-wallet-btn" class=" btn glyphicon glyphicon-ok center-block"></a></p> </form> </div>';


$(document).ready(function () {
    var weekday=new Array(7);
    weekday[0]="Sunday";
    weekday[1]="Monday";
    weekday[2]="Tuesday";
    weekday[3]="Wednesday";
    weekday[4]="Thursday";
    weekday[5]="Friday";
    weekday[6]="Saturday";

    var d = new Date();
    var day = d.getDate();
    var month = d.getMonth() + 1;
    var year = d.getFullYear();
    var dateField = $('.nav-right #date-field');
    dateField.append(month + "/" + day + "/" + year + " (" + weekday[d.getDay()] + ")")
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = getCookie('csrftoken');
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var isWalletAddFormPresent = function(){
    return $("#add-new-wallet-form").length !== 0;
};

var makeFieldBad = function (block,field, text) {
    field.attr("placeholder", text);
    field.val('');
    block.addClass("has-error");
};

var makeFieldOk = function (block) {
    block.removeClass("has-error");
    block.addClass("has-success");
};

var cleanBlock = function (block, field, placeholder) {
    block.removeClass("has-error has-success");
    field.val('');
    field.attr("placeholder", placeholder);
};

var verifyAddWalletFields = function(data){
    if (data.status == '400') {

        var nameGroup =  $("#name-group");
        var nameField = $("#new-wallet-name");

        var typeGroup = $("#type-group");
        var typeField = $("#new-wallet-type");

        var sumGroup =  $("#sum-group");
        var sumField = $("#new-wallet-sum");

        if(typeof data.name !== 'undefined'){
            makeFieldBad(nameGroup,nameField,data.name)
        }
        else{
           makeFieldOk(nameGroup)
        }

        if('type' in data){
            makeFieldBad(typeGroup,typeField,data.type)
        }
        else{
           makeFieldOk(typeGroup)
        }

        if('sum' in data){
            makeFieldBad(sumGroup,sumField,data.sum)
        }
        else {
           makeFieldOk(sumGroup)
        }
    }
    if(data.status == '200')
    {
        $("#add-new-wallet-form").remove();
        refreshWallets();
    }
};

$(function(){
    var button = $("#add-wallet-button");
        button.click(function(){
        if(isWalletAddFormPresent()){
            return;
        }
        $("#add-button-div").before(newWalletForm);
        showBlock($("#add-new-wallet-form"));
        $(function(){
            $("#add-new-wallet-btn").click(function(){
                $.ajax({
                    url: "addwallet/",
                    type: "POST",
                    data: {
                        name: $("#new-wallet-name").val(),
                        type: $("#new-wallet-type").val(),
                        sum: $("#new-wallet-sum").val()
                    },
                    dataType: 'json'})
                .done(verifyAddWalletFields);
                });
            });
        });
});

var getWalletsTitles = function () {
    $.ajax({
        url: "get-wallets-titles/",
        type: "GET",
        dataType: 'json',
        success: function (data) {
            var selectWallets = $("#id_wallets");
           $.each(data, function (iter, value) {
               selectWallets.append( $('<option value='+value.title+'>'+value.title+'</option>'));
           });
            var title = selectWallets.find(":selected").text();
            getSelectWalletCodes(title);
        }
    })
};

$(document).ready(getWalletsTitles());

var getSelectWalletCodes = function (title) {
    $.ajax({
            url: "get-codes-by-wallet-title/",
            type: "GET",
            data: {
                walletTitle: title
            },
            dataType: 'json',
            success: function (data) {
                var code = $("#id_code");
                code.empty();
           $.each(data, function (iter, value) {
               code.append( $("<option value="+iter+">"+value+"</option>"));
           });
            }
        })
};


$(function () {
   var info = $("#id_wallets");
    info.click(function () {
        var title = info.find(":selected").text();
        getSelectWalletCodes(title);
    });
});


var hideBlock = function (block) {
    block.animate({
        opacity: 0
    });
    block.hide();
};

var showBlock = function (block) {
  block.show();
  block.animate({
      opacity: 1
  });
};



var addNewOperation = function () {
    var button = $("#spending-button");
    var operationType = "SP";

    var sumAddon = $("#sum-addon");
    var spendingButton = $("#operation-spending-button");
    var incomButton = $("#operation-incom-button");

    spendingButton.click(function () {
        sumAddon.text("-");
        operationType = "SP";
    });

    incomButton.click(function () {
        sumAddon.text("+");
        operationType = "DP";
    });

    button.click(function () {
    var title = $("#spending-title-input");
    var titleForm = $("#spending-title-form");
    var sum = $("#spending-sum-input");
    var sumForm = $("#spending-sum-form");
    var wallet = $("#id_wallets");
    var code = $("#id_code");
    var date = $("#spending-date-input");
    var dateForm =$("#spending-date-form");
        $.ajax({
            url:"add-new-operation/",
            type:"POST",
            dataType:"json",
            data: {
                type: operationType,
                title: title.val(),
                sum: sum.val(),
                wallet: wallet.find(":selected").text(),
                code: code.find(":selected").text(),
                select_value: code.find(":selected").val(),
                date: date.val()
            },
            success: function (data) {
                 if('sum' in data){
                     makeFieldBad(sumForm, sum, data.sum)
                 }
                 else{
                     makeFieldOk(sumForm)
                 }

                if('name' in data){
                    makeFieldBad(titleForm, title, data.name)
                }
                else{
                    makeFieldOk(titleForm)
                }
                if('date' in data){
                    makeFieldBad(dateForm, date, data.date)
                }
                else{
                    makeFieldOk(dateForm)
                }
                if(data.status == '200')
                {
                    refreshWallets();
                    cleanBlock(sumForm,sum, "Sum");
                    cleanBlock(titleForm,title, "Title");
                    cleanBlock(dateForm, date, "");
                }
            }
        })
    })
};

addNewOperation();

String.prototype.trimAll=function()
{
  var r=/\s+/g;
  return this.replace(r,'');
};


var editWalletTitle = function () {
    var editButton = $(".wallet-block .glyphicon-pencil");
    editButton.click(function () {
        var clickedButton = $(editButton[editButton.index(this)]);
        var title = clickedButton.parents("#wallet-title");
        var textTitle = title.find("h4").text();
        var editField = title.siblings("#edit-title");
        var titleInput = editField.find("#title-input");
        var submitBtn = editField.find('a:last');
        hideBlock(title);
        showBlock(editField);
        submitBtn.click(function () {
            $.ajax({
                url: "edit-wallet-title/",
                type: "POST",
                dataType: "json",
                data: {
                    newTitle: titleInput.val(),
                    oldTitle: textTitle
                },
                success: function (data) {
                   if('title' in data){
                       makeFieldBad(titleInput.parent(), titleInput, data.title)
                    }
                    if(data.status == '200')
                    {
                        refreshWallets();
                    }
                }
            })
        })
    })
};

var addWalletCurrency = function () {
    var addButton = $(".wallet-block .glyphicon-plus");
    addButton.click(function () {
        var btn = $(addButton[addButton.index(this)]);
        var form = btn.siblings("#new-currency");
        var titleForm = btn.siblings("#wallet-title");
        showBlock(form);
        hideBlock(btn);
        var submitBtn = form.find('p:last');

        var codeForm = form.find('#add-currency-input');
        var sumForm = form.find('#add-value-input');

        var title = titleForm.find('h4').text();

        submitBtn.click(function () {
            var code = codeForm.val();
            var sum = sumForm.val();
            $.ajax({
                url:"add-new-currency/",
                type: "POST",
                dataType: 'json',
                data: {
                  title: title,
                  code: code,
                  sum: sum
                },
                success: function (data) {
                    if('type' in data){
                       makeFieldBad(codeForm.parent(), codeForm, data.type)
                    }
                    else{
                        makeFieldOk(codeForm.parent())
                    }

                    if('sum' in data){
                       makeFieldBad(sumForm.parent(), sumForm, data.sum)
                    }
                    else{
                        makeFieldOk(sumForm.parent())
                    }
                    if(data.status == '200')
                    {
                        refreshWallets();
                    }
                }
            })
        })
    })
};


var createWalletDiv = function (title) {
    var div = document.createElement("div");
    var walletDivId = ("id-wallet-" + title).trimAll();
    div.id= walletDivId;
    $("#add-button-div").before(div);
    div = $("#"+walletDivId);
    div.addClass("col-md-2 wallet-block wallet-frame disabled");
    div.append('<div id="wallet-title"> <h4 class="text-overflow">'+title+'<a class="btn-padding btn pull-right glyphicon glyphicon-pencil"></a></h4> </div>');
    div.append('<div id="edit-title" class="disabled edit-title"> <p><input  type="text" id="title-input" class=" form-control input-sm" placeholder="Wallet title"></p>  <a class="btn-padding btn  glyphicon glyphicon-ok center-block"></a> </div>');
    div.append('<hr>');
    div.append('<div id="new-currency" class="form-group disabled">  <p> <input id="add-currency-input" type="text" class=" form-control input-sm" placeholder="Currency (USD,EUR,etc.)"> </p> <p><input id="add-value-input" type="text" class=" form-control input-sm" placeholder="Value"> </p> <p><a class="btn-padding btn  glyphicon glyphicon-ok center-block"></a></p> </div>');
    div.append(' <a class=" btn glyphicon glyphicon-plus center-block"></a>');
};

var fillWallet = function (title, currencyCode, value) {
    var walletDivId = ("id-wallet-" + title).trimAll();
    var div = $("#"+walletDivId);
    var div_button = $("#"+walletDivId +" .form-group");
    div_button.before("<p>"+currencyCode+'<span class="pull-right">'+value+'</span>');
    div_button.before('<hr>');
    showBlock(div);
};

var addWalletsToHtml = function (json_data) {
          $.each(json_data, function (title, element) {
              createWalletDiv(title);
              $.each(element, function (value, code) {
                  fillWallet(title, code, value);
              })
          });
};

var refreshWallets = function () {
    var wallet = $(".wallet-block");
    hideBlock(wallet);
    wallet.remove();
    getAllWallets();
    var select = $("#id_wallets");
    select.empty();
    getWalletsTitles();
};

var getAllWallets = function () {
  $.ajax({
      url:"wallets/",
      type: "GET",
      dataType: "json",
      success: function (data) {
          addWalletsToHtml(data);
          editWalletTitle();
          addWalletCurrency();
      }
  });
};

$(document).ready(getAllWallets());
