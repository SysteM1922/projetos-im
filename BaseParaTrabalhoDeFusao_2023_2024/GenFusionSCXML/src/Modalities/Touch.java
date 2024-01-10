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
public enum Touch implements IModality{

    SHAPE_TRIANGULO("[TOUCH][SHAPE][TRIANGULO]",1500),
    SHAPE_QUADRADO("[TOUCH][SHAPE][QUADRADO]",1500),
    SHAPE_CIRCULO("[TOUCH][SHAPE][CIRCULO]",1500),

  
    ;
    
    private String event;
    private int timeout;


    Touch(String m, int time) {
        event=m;
        timeout=time;
    }

    @Override
    public int getTimeOut() {
        return timeout;
    }

    @Override
    public String getEventName() {
        //return getModalityName()+"."+event;
        return event;
    }

    @Override
    public String getEvName() {
        return getModalityName().toLowerCase()+event.toLowerCase();
    }
    
}