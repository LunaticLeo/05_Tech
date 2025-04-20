try {
    module.exports = {
        check
    };
} catch (error) { }

function check(input, dataType) {
    switch (dataType) {
        case "id":
            if (input == undefined) return false;
            if (typeof (input) != "string") return false;
            input = input.trim();
            input = input.toLowerCase();
            if (input.length == 0) return false;
            if (! /^[0-9a-fA-F]{24}$/.test(input)) return false;

            return input;
        case "name":
            if (input == undefined) return false;
            if (typeof (input) != "string") return false;
            input = input.trim();
            if (input.length == 0) return false;

            return input;
        case "username":
            if (input == undefined) return false;
            if (typeof (input) != "string") return false;
            input = input.trim();
            if (input.length == 0) return false;
            input = input.toLowerCase();

            return input;
        case "password":
            if (input == undefined) return false;
            if (typeof (input) != "string") return false;
            input = input.trim();
            if (input.length == 0) return false;

            return input;
        case "take":
            if (input == undefined) return 20;
            if (typeof (input) == "string") {
                input = input.trim();
                if (input.length == 0) input = "20";
                if (! /^[0-9]+$/.test(input)) return false;
                input = Number(input);
            }
            if (typeof (input) == "number") {
                if (input == 0) return 20;
                if (input > 100) input = 100;
                return input
            }

            return false;
        case "skip":
            if (input == undefined) return 0;
            if (typeof (input) == "string") {
                input = input.trim();
                if (input.length == 0) input = "0";
                if (! /^[0-9]+$/.test(input)) return false;
                input = Number(input);
            }
            if (typeof (input) == "number") {
                if (input < 0) return false;
                return input
            }
            return false;
        case "title":
            if (input == undefined) return false;
            if (typeof (input) != "string") return false;
            input = input.trim();
            if (input.length == 0) return false;

            return input;
        case "body":
            if (input == undefined) return false;
            if (typeof (input) != "string") return false;
            input = input.trim();
            if (input.length == 0) return false;

            return input;
        case "comment":
            if (input == undefined) return false;
            if (typeof (input) != "string") return false;
            input = input.trim();
            if (input.length == 0) return false;

            return input;
        default:
            return false;
    }
}

// console.log(check(undefined, "take"));