/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('pos_order_backup.chrome', function (require) {
    "use strict";
    var chrome = require("point_of_sale.chrome");

    chrome.StatusWidget.include({
        set_status: function(status,msg){
            console.log(status,msg);
            this._super(status,msg);
            ['disconnected','warning','error'].includes(status) && $(".order-backup-btn").show() || $(".order-backup-btn").hide();
        },
    });

    var OrderBackupWidget = chrome.StatusWidget.extend({
        template: 'OrderBackupWidget',
        start: function(){
            var self = this;
            this.$el.click(function(){
                self.pos.gui.show_popup("order_backup_popup", {});
            });
        },
    });

    chrome.Chrome.prototype.widgets.unshift({
        'name':   'pos_order_backup',
        'widget': OrderBackupWidget,
        'append':  '.pos-rightheader',
    });
});