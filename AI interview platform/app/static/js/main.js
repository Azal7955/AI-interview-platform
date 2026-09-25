document.addEventListener(
    "DOMContentLoaded",
    function () {

        const messages =
            document.querySelectorAll(
                ".flash"
            );

        messages.forEach(
            function (message) {

                setTimeout(
                    function () {

                        message.remove();

                    },
                    4500
                );

            }
        );

    }
);