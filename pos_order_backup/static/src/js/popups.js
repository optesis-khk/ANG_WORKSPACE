/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('pos_order_backup.popups', function (require) {
    "use strict";
    var gui = require('point_of_sale.gui');
    var popup_widget = require('point_of_sale.popups');

    var OrderBackupPopup = popup_widget.extend({
        template: 'OrderBackupPopup',

        events: {
            'click .cancel' : 'click_cancel',
            'click #backup-order' : 'backup_cache',
            'click #clear-cache' : 'clear_cache',
            'click .order-clear-ok' : 'confirm_clear_cache',
        },
        confirm_clear_cache: function(){
            this.pos.db.clear_cached_orders();
            this.pos.push_order(null,{'show_error':true});
            this.click_cancel();
        },
        show_second_set: function(){
            this.$(".backup-popup-one").hide();
            this.$(".backup-popup-two").show();
        },
        show_third_set: function(){
            this.$(".backup-popup-one").hide();
            this.$(".backup-popup-three").show();
        },
        backup_cache: function(){
            this.pos.db.download_cached_orders(this.pos.pos_session.name.toString());
            this.show_third_set();
        },
        clear_cache: function(){
            this.show_second_set();
        },
    });
    gui.define_popup({name:'order_backup_popup', widget: OrderBackupPopup});
});