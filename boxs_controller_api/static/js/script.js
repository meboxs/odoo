            // Set the target date and time (in UTC)
            var targetDate_now = new Date();

            var myDivValue = document.getElementById("set_time").innerHTML;

            targetDate_now.setMinutes(targetDate_now.getMinutes() + parseInt(myDivValue));

            // Update the countdown every second
            var countdown = setInterval(function() {

            // Get the current date and time
            var now = new Date().getTime();

            // Calculate the time remaining
            var timeRemaining = targetDate_now - now;

            // Calculate days, hours, minutes, and seconds remaining
            var days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
            var hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

            // Construct the countdown display
            // var countdownDisplay ="Auto reload : "+ days + "d " + hours + "h " + minutes + "m " + seconds + "s";
            var countdownDisplay ="Auto reload : "+   minutes + "m " + seconds + "s";
            // Display the countdown
            document.getElementById("countdown").innerHTML = countdownDisplay;

            // If the countdown is over, display a message
            if (timeRemaining < 0) {
                    clearInterval(countdown);
                    location.reload();
                    }
                }, 1000);