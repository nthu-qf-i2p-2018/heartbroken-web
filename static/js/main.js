$(document).ready(function() {
    PlayerBtn.text('開始').click(startGame);
});

var SuitName = {'♣': 'clubs', '♦': 'diamonds', '♠': 'spades', '♥': 'hearts'}
var PlayerBtn = $("#player button.btn");

function startGame() {
    $.ajax({
        type: "POST",
        url: "play",
        data: JSON.stringify({}),
        dataType: 'json',
        success: function(data) {
            PlayerBtn.off();
            // reset desk
            $(".player .card").attr("class", "card empty");
            doJob(data);
        }, 
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            console.log("Status: " + textStatus); 
            console.log("Error: " + errorThrown); 
        } 
    });
}

function doJob(data) {
    if(data.instruction == 'pass card') {
        renderCards(data.cards_you_have);
        PlayerBtn.text('換牌').prop('disabled', true).click(function() {
            if(!$(this).prop('disabled')) {
                var cards = $(this).parent().find('.card.selected').map(function() {
                    var card = $(this).attr("alt");
                    return {"suit": card[0], "number": parseInt(card.slice(1))};
                }).toArray();
                passCards(cards);   
            }
        });
        // set click function for card click
        $("#player .card").click(function() {
            $(this).toggleClass('selected');
            var okToPass = $(this).parent().find('.card.selected').length == 3;
            PlayerBtn.prop('disabled', !okToPass);
        });
    } else if (data.instruction == "play card") {
        PlayerBtn.hide();
        renderCards(data.cards_you_have);

        // TODO: display the result of last round
        if(data.history.length > 0 && data.msg != 'Illegal move!') {
            last_round = data.history.slice(-1);
            // TODO: show all cards played last round
            // TODO: show the winner last round (move cards to the position)
        }

        // reset desk
        $(".player .card").attr("class", "card empty");

        // TODO: display card is played 1-by-1 (animation)
        data.cards_played.forEach(function(card, index, array) {
            var n = array.length - index;
            var suitName = SuitName[card.suit];
            $(`.player-${n} .card`).removeClass('empty').addClass(suitName).addClass(`rank${card.number}`);
        });
        // set click function for card click
        $("#player .card").click(function() {
            var card = $(this).attr("alt");
            playCard(card);
            $(this).remove();
        });
    } else if (data.instruction == 'end') {
        renderCards([]);
        alert(data.scores);
        PlayerBtn.text('重新開始').click(startGame).fadeIn();
        PlayerBtn.prop('disabled', false);
    }
}

function renderCards(cards) {
    var htmlFrag = '';
    cards.forEach(function(card) {
        var suit = SuitName[card.suit];
        htmlFrag += `<div class="card ${suit} rank${card.number}" alt="${card.suit}${card.number}">
                        <div class="face"></div>
                    </div>`;
    });
    $("#player .cards").html(htmlFrag);
}

function passCards(cards) {
    PlayerBtn.prop('disabled', true);
    var data = JSON.stringify({"cards": cards});
    $.ajax({
        type: "POST",
        url: "play",
        data: data,
        dataType: 'json',
        success: function(data) {
            PlayerBtn.hide();
            doJob(data);
        }, 
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            var okToPass = $(this).parent().find('.card.selected').length == 3;
            PlayerBtn.prop('disabled', !okToPass);
            console.log("Status: " + textStatus); 
            console.log("Error: " + errorThrown); 
        } 
    });
}

function playCard(card) {
    var suit = card[0]
    var suitName = SuitName[suit];
    var number = parseInt(card.slice(1));
    $('.player-0 .card').removeClass('empty').addClass(suitName).addClass(`rank${number}`);
    var data = JSON.stringify({"card": {"suit": suit, "number": number}});
    $.ajax({
        type: "POST",
        url: "play",
        data: data,
        dataType: 'json',
        success: doJob,
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            console.log("Status: " + textStatus); 
            console.log("Error: " + errorThrown); 
        } 
    });
}

// TODO: show message tooltip
function showMsg(msg) {
}