$(document).ready(function() {
    PlayerBtn.text('開始').click(startGame);
});

var SuitName = {'♣': 'clubs', '♦': 'diamonds', '♠': 'spades', '♥': 'hearts'}
var PlayerBtn = $("#user button.btn");

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
        setPassCard();
    } else if (data.instruction == "play card") {
        renderCards(data.cards_you_have);
        data.scores.forEach(function(score, index, array) {
            $(`.player-${index} .score`).text(score);
        });

        var timeout = 0;
        if(data.history.length > 0) {
            renderLastRound(data.history);
            timeout = 2000;
        }
        setTimeout(startNewRound.bind(null, data.cards_played), timeout)
    } else if (data.instruction == 'end') {
        renderCards([]);
        renderLastRound(data.history);
        PlayerBtn.text('重新開始').click(startGame).fadeIn();
        PlayerBtn.prop('disabled', false);
    }
}

function startNewRound(cards) {
    // reset table
    $(".player .card").attr("class", "card empty");

    // TODO: display card is played 1-by-1 (animation)
    cards.forEach(function(card, index, array) {
        var n = 4 - array.length + index;
        $(`.player-${n} .card`).removeClass('empty').addClass(SuitName[card.suit]).addClass(`rank${card.number}`);
    });

    // set click function for card click
    $("#user .card").click(function() {
        playCard($(this).attr("alt"));
    });
}

function setPassCard() {
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
    $("#user .card").click(function() {
        $(this).toggleClass('selected');
        var okToPass = $('#user .card.selected').length == 3;
        PlayerBtn.prop('disabled', !okToPass);
    });
}

function renderLastRound(history) {
    play_infos = history.slice(-1)[0];
    play_infos.forEach(function(play_info, index, array) {
        var n = play_info[0];
        var card = play_info[1];
        $(`.player-${n} .card`).removeClass('empty').addClass(SuitName[card.suit]).addClass(`rank${card.number}`);
    });
    // TODO: show all cards played last round
    // TODO: show the winner last round (move cards to the position)
}

function renderCards(cards) {
    var htmlFrag = '';
    cards.forEach(function(card) {
        var suit = SuitName[card.suit];
        htmlFrag += `<div class="card ${suit} rank${card.number}" alt="${card.suit}${card.number}">
                        <div class="face"></div>
                    </div>`;
    });
    $("#user .cards").html(htmlFrag);
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