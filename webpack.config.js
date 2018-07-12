const path = require('path');

module.exports = {
    entry: './static/css/app.css',
    output: {
        filename: 'style-bundle.js',
    },

    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: './static/css/dist/bundle.css',
                        }
                    },
                    { loader: 'extract-loader' },
                    { loader: 'css-loader' },
                ]
            }
        ]
    },
};