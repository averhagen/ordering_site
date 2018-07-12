const path = require('path');

module.exports = {
    entry: './static/css/app.css',
    output: {
        filename: './static/dist/js/style-bundle.js',
    },

    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: './static/dist/css/bundle.css',
                        }
                    },
                    { loader: 'extract-loader' },
                    { loader: 'css-loader' },
                ]
            }
        ]
    },
};