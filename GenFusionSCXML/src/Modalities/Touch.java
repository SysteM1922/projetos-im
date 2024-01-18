/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package Modalities;

import scxmlgen.interfaces.IModality;

/**
 *
 * @author nunof
 */
public enum Touch implements IModality {

    // SHAPE_TRIANGULO("[TOUCH][SHAPE][TRIANGULO]", 1500),
    // SHAPE_QUADRADO("[TOUCH][SHAPE][QUADRADO]", 1500),
    // SHAPE_CIRCULO("[TOUCH][SHAPE][CIRCULO]", 1500),

    QUIT_APP("[GESTURES][CONTINENCE]", 2000),
    SCROLL_UP("[GESTURES][SCROLLDR]", 2000),
    SCROLL_DOWN("[GESTURES][SCROLLUR]", 2000),
    OPEN_PRODUCT("[GESTURES][PUSHF]", 2000),

    ASK_HELP("[GESTURES][RAISERH]", 5000),

    ADD_TO_CART("[GESTURES][TRANSPORTR]", 5000),

    ;

    private String event;
    private int timeout;

    Touch(String m, int time) {
        event = m;
        timeout = time;
    }

    @Override
    public int getTimeOut() {
        return timeout;
    }

    @Override
    public String getEventName() {
        // return getModalityName()+"."+event;
        return event;
    }

    @Override
    public String getEvName() {
        return getModalityName().toLowerCase() + event.toLowerCase();
    }

}