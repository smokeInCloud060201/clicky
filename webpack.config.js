const path = require("path");
const CopyPlugin = require("copy-webpack-plugin");

module.exports = {
    mode: "production",
    entry: {
        content: "./src/content.js"
    },
    output: {
        filename: "[name].js",
        path: path.resolve(__dirname, "dist")
    },
    plugins: [
        new CopyPlugin({
            patterns: [
                { from: "manifest.json", to: "." }
            ]
        })
    ]
};
