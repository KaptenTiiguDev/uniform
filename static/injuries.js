class BodyUI {

    constructor() {
        this.torsoImage = '../static/body3.png';
        this.leftHandImage = '../static/body3_left_hand.png';
        this.rightHandImage = '../static/body3_right_hand.png';
    }

    setLeftHandGone() {
        this.leftHandImage = '../static/body3_left_hand_gone.png';
    }

    getLeftHandGone() {
        return '../static/body3_left_hand_gone.png';
    }

    setLeftHandNormal() {
        this.leftHandImage = '../static/body3_left_hand.png';
    }

    setRightHandGone() {
        this.rightHandImage = '../static/body3_right_hand_gone.png';
    }

    getRightHandGone() {
        return '../static/body3_right_hand_gone.png';
    }

    setRightHandNormal() {
        this.rightHandImage = '../static/body3_right_hand.png';
    }

    setHandNormal(bodyPart) {
        if (bodyPart === 'leftArm') {
            this.setLeftHandNormal();
        }  else if (bodyPart === 'rightArm') {
            this.setRightHandNormal();
        }
    }

    setHandGone(bodyPart) {
        if (bodyPart === 'leftArm') {
            this.setLeftHandGone();
        }  else if (bodyPart === 'rightArm') {
            this.setRightHandGone();
        }
    }
}

class APIResponse {
    constructor(bodyPart, injury, injuryType, instructions) {
        this.bodyPart = bodyPart;
        this.injury = injury;
        this.injuryType = injuryType;
        this.instructions = instructions;
    }
}

class Animator {
    constructor(imgUrl, className) {
        this.className = className;
        this.imgUrl = imgUrl;
        this.replacementImg = className === '#body-right-arm' ? '../static/body3_right_hand.png' : '../static/body3_left_hand.png';
        this.interval = null;
        this.switch = false;
    }

    startAnimation() {
        // console.log('start animation' + this.className);
        this.interval = setInterval(() => {
            this.switch = !this.switch;
            let imgUrl = this.switch ? this.imgUrl : this.replacementImg;
            $(this.className).attr("src", imgUrl);
        }, 500);
    }

    stopAnimation() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}

class BodySystem {
    constructor() {
        this.instructions = [];
        this.injuries = [];
        this.bodyUI = new BodyUI();
        this.leftHandAnimator = new Animator(this.bodyUI.getLeftHandGone(), "#body-left-arm");
        this.rightHandAnimator = new Animator(this.bodyUI.getRightHandGone(), "#body-right-arm");
    }

    updateInjury(apiResponse) {
        if (apiResponse.injuryType === 0) {
            this.bodyUI.setHandNormal(apiResponse.bodyPart);
        } else {
            this.instructions = this.instructions.concat(apiResponse.instructions);
            this.injuries.push(apiResponse.injury);
            if (apiResponse.injuryType === 1) {
                this.bodyUI.setHandNormal(apiResponse.bodyPart);
            } else {
                this.bodyUI.setHandGone(apiResponse.bodyPart);
            }
        }
    }

    updateUI() {
        this.resetInstructions();
        this.resetInjuries();
        // display instructions
        for (let i = 0; i < this.instructions.length; i++) {
            $('#injury-info-text-' + i).html(this.instructions[i]);
            $('#injury-info-container-' + i).css('display', 'flex');
        }
        // display injuries
        for (let i = 0; i < this.injuries.length; i++) {
            $('#injury-text-' + i).html(this.injuries[i]);
            $('#injury-text-container-' + i).css('display', 'flex');
        }

        // hack
        if (
            (this.bodyUI.leftHandImage === '../static/body3_left_hand.png' && this.bodyUI.rightHandImage === '../static/body3_right_hand_gone.png' && this.injuries.length > 1)
            || (this.bodyUI.leftHandImage === '../static/body3_left_hand.png' && this.bodyUI.rightHandImage !== '../static/body3_right_hand_gone.png' && this.injuries.length)
        ) {
            this.showBleedingAnimation({bodyPart: 'leftArm'});
        } else {
            this.hideBleedingAnimation();
        }


        // another hack
        if (this.bodyUI.rightHandImage === '../static/body3_right_hand_gone.png' && !this.rightHandAnimator.interval) {
            this.rightHandAnimator.startAnimation();
        } else if (this.bodyUI.rightHandImage !== '../static/body3_right_hand_gone.png' && this.rightHandAnimator.interval) {
            this.rightHandAnimator.stopAnimation();
            $("#body-right-arm").attr("src", this.bodyUI.rightHandImage);
        } else if (this.bodyUI.rightHandImage !== '../static/body3_right_hand_gone.png' && !this.rightHandAnimator.interval) {
            $("#body-right-arm").attr("src", this.bodyUI.rightHandImage);
        }

        if (this.bodyUI.leftHandImage === '../static/body3_left_hand_gone.png' && !this.leftHandAnimator.interval) {
            this.leftHandAnimator.startAnimation()
        } else if (this.bodyUI.leftHandImage !== '../static/body3_left_hand_gone.png' && this.leftHandAnimator.interval) {
            this.leftHandAnimator.stopAnimation();
            $("#body-left-arm").attr("src", this.bodyUI.leftHandImage);
        } else if (this.bodyUI.leftHandImage !== '../static/body3_left_hand_gone.png' && !this.leftHandAnimator.interval) {
            $("#body-left-arm").attr("src", this.bodyUI.leftHandImage);
        }
    }

    resetInjuries() {
        $('#injury-text-0').html('');
        $('#injury-text-container-0').hide();
        $('#injury-text-1').html('');
        $('#injury-text-container-1').hide();
        $('#injury-text-2').html('');
        $('#injury-text-container-2').hide();
    }

    resetInstructions() {
        $('#injury-info-text-0').html('');
        $('#injury-info-container-0').hide();
        $('#injury-info-text-1').html('');
        $('#injury-info-container-1').hide();
        $('#injury-info-text-2').html('');
        $('#injury-info-container-2').hide();
    }

    showBleedingAnimation(data) {
        $('#body-spot-' + data.bodyPart).show();
    }

    hideBleedingAnimation() {
        $('.body-spot').hide();
    }
}

bodySystem = new BodySystem();

function updateData() {

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:5000/injuries",
        success: function (dataList) {
            if ($.isEmptyObject(dataList)) return;
            bodySystem.instructions = [];
            bodySystem.injuries = [];
            for (let data of dataList) {
                let res = new APIResponse(data['bodyPart'], data['injury'], data['injuryType'], data['instructions']);
                bodySystem.updateInjury(res);
            }
            bodySystem.updateUI();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            // console.log(jqXHR.status);
        }
    });

}

$(document).ready(function () {

    setInterval(function () {
        updateData();
    }, 300)

});
