/*
 * DualPowerGeneration.c
 *
 * Created: 10/11/2019 5:07:09 PM
 * Author : Brandon Fong        <- Joseph Was here :3
 * 
 *
 * Date last modified: 
 */ 
//We want four resistors but lets first get the logic down for two
//Using res0, res1 (i.e. photoresistor 1 and 2)
//We are assuming the axis of rotation is one fixed motion
//Consider:  frequency to sample.  the amount we sample affects power efficiency
//Joseph's diagram is on google drive


#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "Param_Const_GLVar.h"

int main(void)
{
	//Initialize
	initTimer0(); // Initializing timer 0
	initTimer1(); // Initializing timer 1
	initTimer2(); // Initializing timer 2
	adc_init(); // Initializing ADC
	dac_init(); // Initializing DAC
	sei();
	
    while (1) {}
}








