/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 * @attention
 *
 * <h2><center>&copy; Copyright (c) 2021 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under Ultimate Liberty license
 * SLA0044, the "License"; You may not use this file except in compliance with
 * the License. You may obtain a copy of the License at:
 *                             www.st.com/SLA0044
 *
 ******************************************************************************
 */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "cmsis_os.h"
#include "usb_device.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "usbd_cdc_if.h"
#include "string.h"
#include <stdio.h>
#include "../Inc/printf.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

I2S_HandleTypeDef hi2s2;
I2S_HandleTypeDef hi2s3;

SPI_HandleTypeDef hspi1;

osThreadId defaultTaskHandle;
/* USER CODE BEGIN PV */

//float tMagMeritev[4];
//float tAccMeritev[4];
//float tGyroMeritev[4];

TaskHandle_t xMagHandle = NULL;
TaskHandle_t xAccHandle = NULL;
TaskHandle_t xGyroHandle = NULL;
TaskHandle_t xPrintHandle = NULL;

QueueHandle_t xQueue = NULL;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_I2S2_Init(void);
static void MX_I2S3_Init(void);
static void MX_SPI1_Init(void);
void StartDefaultTask(void const *argument);

/* USER CODE BEGIN PFP */
uint8_t i2c1_pisiMagReg(uint8_t, uint8_t, uint8_t);
void i2c1_beriMagReg(uint8_t, uint8_t, uint8_t*, uint8_t);
void initMagnetometer(void);

uint8_t i2c1_pisiAccReg(uint8_t, uint8_t, uint8_t);
void i2c1_beriAccReg(uint8_t, uint8_t, uint8_t*, uint8_t);
void initAccelmeter(void);

uint8_t spi1_beriRegister(uint8_t);
void spi1_beriRegistre(uint8_t, uint8_t*, uint8_t);
void spi1_pisiRegister(uint8_t, uint8_t);
void initGyro(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

//
//Mag functions
uint8_t i2c1_pisiMagReg(uint8_t naprava, uint8_t reg, uint8_t podatek) {
	naprava <<= 1;
	return HAL_I2C_Mem_Write(&hi2c1, naprava, reg, I2C_MEMADD_SIZE_8BIT,
			&podatek, 1, 10);
}

void i2c1_beriMagReg(uint8_t naprava, uint8_t reg, uint8_t *podatek,
		uint8_t dolzina) {
	if ((dolzina > 1) && (naprava == 0x1e)) // ce je naprava 0x19 moramo postaviti ta bit, ce zelimo brati vec zlogov
		reg |= 0x80;
	naprava <<= 1;
	HAL_I2C_Mem_Read(&hi2c1, naprava, reg, I2C_MEMADD_SIZE_8BIT, podatek,
			dolzina, dolzina);
}

void initMagnetometer() {
	HAL_Delay(10);

// Za potrebe testa, moramo testni napravi sporoviti kateri senzor imamo
//#define OLD_SENSOR 0x73 // Odkomentiramo za LSM303DLHC / stari senzor
#define NEW_SENSOR 0x6E // Odkomentiramo za LSM303AGR / novi senzor

#if defined(OLD_SENSOR) && !defined(NEW_SENSOR)
  i2c1_pisiMagReg(0x1e, 0x4F, OLD_SENSOR); // Povemo testni napravi, da imamo stari senzor
#elif !defined(OLD_SENSOR) && defined(NEW_SENSOR)
	i2c1_pisiMagReg(0x1e, 0x4F, NEW_SENSOR); // Povemo testni napravi, da imamo novi senzor
#else
  for(;;); // V primeru napake, pocakamo tukaj
#endif
	HAL_Delay(100);

	// inicializiraj pospeskometer
	i2c1_pisiMagReg(0x1E, 0x60, 0x84);
}

//
//Acc functions
uint8_t i2c1_pisiAccReg(uint8_t naprava, uint8_t reg, uint8_t podatek) {
	naprava <<= 1;
	return HAL_I2C_Mem_Write(&hi2c1, naprava, reg, I2C_MEMADD_SIZE_8BIT,
			&podatek, 1, 10);
}

void i2c1_beriAccReg(uint8_t naprava, uint8_t reg, uint8_t *podatek,
		uint8_t dolzina) {
	if ((dolzina > 1) && (naprava == 0x19)) // ce je naprava 0x19 moramo postaviti ta bit, ce zelimo brati vec zlogov
		reg |= 0x80;
	naprava <<= 1;
	HAL_I2C_Mem_Read(&hi2c1, naprava, reg, I2C_MEMADD_SIZE_8BIT, podatek,
			dolzina, dolzina);
}

void initAccelmeter() {
	HAL_Delay(10);

// Za potrebe testa, moramo testni napravi sporoviti kateri senzor imamo
//#define OLD_SENSOR 0x73 // Odkomentiramo za LSM303DLHC / stari senzor
#define NEW_SENSOR 0x6E // Odkomentiramo za LSM303AGR / novi senzor

#if defined(OLD_SENSOR) && !defined(NEW_SENSOR)
  i2c1_pisiAccReg(0x1e, 0x4F, OLD_SENSOR); // Povemo testni napravi, da imamo stari senzor
#elif !defined(OLD_SENSOR) && defined(NEW_SENSOR)
	i2c1_pisiAccReg(0x1e, 0x4F, NEW_SENSOR); // Povemo testni napravi, da imamo novi senzor
#else
  for(;;); // V primeru napake, pocakamo tukaj
#endif
	HAL_Delay(100);

	// inicializiraj pospeskometer
	i2c1_pisiAccReg(0x19, 0x20, 0x47);  // zbudi pospeskometer in omogoci osi
	i2c1_pisiAccReg(0x19, 0x23, 0x98); // nastavi posodobitev samo ko se prebere vrednost ter visoko locljivost
}

//
//gyro functions
void pavza() {
	uint32_t counter = 0;
	for (counter = 0; counter < 100; counter++) {
		asm("nop");
	}
}

uint8_t spi1_beriRegister(uint8_t reg) {
	uint16_t buf_out, buf_in;
	reg |= 0x80; // najpomembnejsi bit na 1
	buf_out = reg; // little endian, se postavi na pravo mesto ....
	HAL_GPIO_WritePin(GPIOE, GPIO_PIN_3, GPIO_PIN_RESET);
	pavza();
	//HAL_SPI_TransmitReceive(&hspi1, (uint8_t*)&buf_out, (uint8_t*)&buf_in, 2, 2); // blocking posiljanje ....
	HAL_SPI_TransmitReceive(&hspi1, &((uint8_t*) &buf_out)[0],
			&((uint8_t*) &buf_in)[0], 1, 2); // razbito na dva dela, da se podaljsa cas in omogoci pravilno delovanje testa
	pavza();
	HAL_SPI_TransmitReceive(&hspi1, &((uint8_t*) &buf_out)[1],
			&((uint8_t*) &buf_in)[1], 1, 2); // razbito na dva dela, da se podaljsa cas in omogoci pravilno delovanje testa
	HAL_GPIO_WritePin(GPIOE, GPIO_PIN_3, GPIO_PIN_SET);
	pavza();
	return buf_in >> 8; // little endian...
}

void spi1_pisiRegister(uint8_t reg, uint8_t vrednost) {
	uint16_t buf_out;
	buf_out = reg | (vrednost << 8); // little endian, se postavi na pravo mesto ....
	HAL_GPIO_WritePin(GPIOE, GPIO_PIN_3, GPIO_PIN_RESET);
	pavza();
	//HAL_SPI_Transmit(&hspi1, (uint8_t*)&buf_out, 2, 2); // blocking posiljanje ....
	HAL_SPI_Transmit(&hspi1, &((uint8_t*) &buf_out)[0], 1, 2); // razbito na dva dela, da se podaljsa cas in omogoci pravilno delovanje testa
	pavza();
	HAL_SPI_Transmit(&hspi1, &((uint8_t*) &buf_out)[1], 1, 2); // razbito na dva dela, da se podaljsa cas in omogoci pravilno delovanje testa
	HAL_GPIO_WritePin(GPIOE, GPIO_PIN_3, GPIO_PIN_SET);
	pavza();
}

void spi1_beriRegistre(uint8_t reg, uint8_t *buffer, uint8_t velikost) {
	reg |= 0xC0; // najpomembnejsa bita na 1
	HAL_GPIO_WritePin(GPIOE, GPIO_PIN_3, GPIO_PIN_RESET);
	pavza();
	HAL_SPI_Transmit(&hspi1, &reg, 1, 10); // blocking posiljanje....
	pavza();
	HAL_SPI_Receive(&hspi1, buffer, velikost, velikost); // blocking posiljanje....
	HAL_GPIO_WritePin(GPIOE, GPIO_PIN_3, GPIO_PIN_SET);
	pavza();
}

void initGyro() {
	// preverimo ali smo "poklicali" pravi senzor
	uint8_t cip = spi1_beriRegister(0x0F);
	if (cip != 0xD4 && cip != 0xD3) {
		for (;;)
			;
	}

	spi1_pisiRegister(0x20, 0x4F); // 4 - nastavitev za 190Hz | F - zbudi ziroskop in omogoci osi
	spi1_pisiRegister(0x23, 0x10); // 0001 0000 - nastavitev za 500dps
}

//
//tasks
void vTaskMagnetometer(void *pvParameters) {
	/*The parameter value is expected to be 1 as 1 is passed in the
	 pvParameters value in the call to xTaskCreate() below.
	 configASSERT( ( ( uint32_t ) pvParameters ) == 1 );*/

	__HAL_I2C_ENABLE(&hi2c1);
	initMagnetometer();
	int16_t magMeritev[4];
	magMeritev[0] = 0xaaab;
	int8_t packetCounter = 0;
	//TickType_t xLastWakeTime;
	float tMagMeritev[4];

	for (;;) {
		magMeritev[1] = packetCounter++;
		i2c1_beriMagReg(0x1e, 0x68, (uint8_t*) &magMeritev[2], 6);

		tMagMeritev[1] = ((float) magMeritev[2]) * 1.5 * 0.001;
		tMagMeritev[2] = ((float) magMeritev[3]) * 1.5 * 0.001;
		tMagMeritev[3] = ((float) magMeritev[4]) * 1.5 * 0.001;

		xQueueSend(xQueue, &tMagMeritev[0], portMAX_DELAY);
		xQueueSend(xQueue, &tMagMeritev[1], portMAX_DELAY);
		xQueueSend(xQueue, &tMagMeritev[2], portMAX_DELAY);
		xQueueSend(xQueue, &tMagMeritev[3], portMAX_DELAY);

		vTaskSuspend(xMagHandle);
		vTaskResume(xAccHandle);
	}
}

void vTaskAccel(void *pvParameters) {
	/*The parameter value is expected to be 1 as 1 is passed in the
	 pvParameters value in the call to xTaskCreate() below.
	 configASSERT( ( ( uint32_t ) pvParameters ) == 1 );*/

	__HAL_I2C_ENABLE(&hi2c1);
	initAccelmeter();
	int16_t accMeritev[4];
	accMeritev[0] = 0xaaab;
	int8_t packetCounter = 0;
	//TickType_t xLastWakeTime;
	float tAccMeritev[4];

	for (;;) {
		accMeritev[1] = packetCounter++;
		i2c1_beriAccReg(0x19, 0x28, (uint8_t*) &accMeritev[2], 6);

		tAccMeritev[1] = ((float) accMeritev[2]) * 8 / 65536;
		tAccMeritev[2] = ((float) accMeritev[3]) * 8 / 65536;
		tAccMeritev[3] = ((float) accMeritev[4]) * 8 / 65536;

		xQueueSend(xQueue, &tAccMeritev[0], portMAX_DELAY);
		xQueueSend(xQueue, &tAccMeritev[1], portMAX_DELAY);
		xQueueSend(xQueue, &tAccMeritev[2], portMAX_DELAY);
		xQueueSend(xQueue, &tAccMeritev[3], portMAX_DELAY);

		vTaskSuspend(xAccHandle);
		vTaskResume(xGyroHandle);
	}
}

void vTaskGyro(void *pvParameters) {
	/*The parameter value is expected to be 1 as 1 is passed in the
	 pvParameters value in the call to xTaskCreate() below.
	 configASSERT( ( ( uint32_t ) pvParameters ) == 1 );*/

	__HAL_SPI_ENABLE(&hspi1);
	HAL_GPIO_WritePin(GPIOE, GPIO_PIN_3, GPIO_PIN_SET); // CS postavimo na 1
	initGyro();

	int16_t gyroMeritev[6];
	gyroMeritev[0] = 0xaaab;
	int8_t packetCounter = 0;
	float tGyroMeritev[4];

	for (;;) {
		//oznacitev paketa
		gyroMeritev[1] = packetCounter;
		//branje x,y,z
		spi1_beriRegistre(0x28, (uint8_t*) &gyroMeritev[2], 6);
		//operacija, da dobimo dps
		tGyroMeritev[1] = gyroMeritev[2] * 0.0175;
		tGyroMeritev[2] = gyroMeritev[3] * 0.0175;
		tGyroMeritev[3] = gyroMeritev[4] * 0.0175;

		xQueueSend(xQueue, &tGyroMeritev[0], portMAX_DELAY);
		xQueueSend(xQueue, &tGyroMeritev[1], portMAX_DELAY);
		xQueueSend(xQueue, &tGyroMeritev[2], portMAX_DELAY);
		xQueueSend(xQueue, &tGyroMeritev[3], portMAX_DELAY);

		vTaskSuspend(xGyroHandle);
	}
}

void vTaskPrint(void *pvParameters) {
	/*The parameter value is expected to be 1 as 1 is passed in the
	 pvParameters value in the call to xTaskCreate() below.
	 configASSERT( ( ( uint32_t ) pvParameters ) == 1 );*/

	//TickType_t xLastWakeTime;
	//char buffer2[1024];
	//uint32_t dolzina2;

	char buffer[1024];
	uint32_t dolzina;

	float tmpArray[12];
	for (;;) {
		for(int i = 0; i < 3; i++){
			xQueueReceive(xQueue, &tmpArray[0], 0);
			if(tmpArray[0] > -0.1 && tmpArray[0] < 0.1){
				xQueueReceive(xQueue, &tmpArray[1], 0);
				xQueueReceive(xQueue, &tmpArray[2], 0);
				xQueueReceive(xQueue, &tmpArray[3], 0);
			}
			else if(tmpArray[0] > 0.9 && tmpArray[0] < 1.1){
				xQueueReceive(xQueue, &tmpArray[5], 0);
				xQueueReceive(xQueue, &tmpArray[6], 0);
				xQueueReceive(xQueue, &tmpArray[7], 0);
			}
			else{
				xQueueReceive(xQueue, &tmpArray[9], 0);
				xQueueReceive(xQueue, &tmpArray[10], 0);
				xQueueReceive(xQueue, &tmpArray[11], 0);
			}
		}

		/*xQueueReceive(xQueue, &tmpArray[4], 0);

		xQueueReceive(xQueue, &tmpArray[5], 0);
		xQueueReceive(xQueue, &tmpArray[6], 0);
		xQueueReceive(xQueue, &tmpArray[7], 0);
		xQueueReceive(xQueue, &tmpArray[8], 0);
		xQueueReceive(xQueue, &tmpArray[9], 0);
		xQueueReceive(xQueue, &tmpArray[10], 0);
		xQueueReceive(xQueue, &tmpArray[11], 0);*/



		dolzina = sprintf(buffer, "{MAG:{%.3f %.3f %.3f},ACC:{%.3f %.3f %.3f},GYRO:{%.3f %.3f %.3f}}\n\r",
						(float) tmpArray[1], (float) tmpArray[2], (float) tmpArray[3],
						(float) tmpArray[5], (float) tmpArray[6], (float) tmpArray[7],
						(float) tmpArray[9], (float) tmpArray[10], (float) tmpArray[11]);
		//printf("t array %s", buffer);

		/*dolzina2 = sprintf(buffer2, "{MAG:{%.3f %.3f %.3f},ACC:{%.3f %.3f %.3f},GYRO:{%.3f %.3f %.3f}}\n\r",
						(float) tMagMeritev[1], (float) tMagMeritev[2], (float) tMagMeritev[3],
						(float) tAccMeritev[1], (float) tAccMeritev[2], (float) tAccMeritev[3],
						(float) tGyroMeritev[1], (float) tGyroMeritev[2],(float) tGyroMeritev[3]);
		printf("x queue %s", buffer2);*/

		CDC_Transmit_FS((uint8_t*) &buffer, dolzina);
		//vTaskDelayUntil(&xLastWakeTime, 1000);
		//vTaskSuspend(xPrintHandle);
		vTaskResume(xMagHandle);
	}
}

/* USER CODE END 0 */

/**
 * @brief  The application entry point.
 * @retval int
 */
int main(void) {
	/* USER CODE BEGIN 1 */

	/* USER CODE END 1 */

	/* MCU Configuration--------------------------------------------------------*/

	/* Reset of all peripherals, Initializes the Flash interface and the Systick. */
	HAL_Init();

	/* USER CODE BEGIN Init */

	/* USER CODE END Init */

	/* Configure the system clock */
	SystemClock_Config();

	/* USER CODE BEGIN SysInit */

	/* USER CODE END SysInit */

	/* Initialize all configured peripherals */
	MX_GPIO_Init();
	MX_I2C1_Init();
	MX_I2S2_Init();
	MX_I2S3_Init();
	MX_SPI1_Init();
	/* USER CODE BEGIN 2 */
	tMagMeritev[0] = (float)0;
	tAccMeritev[0] = (float)1;
	tGyroMeritev[0] = (float)2;

	BaseType_t xMagReturned;
	BaseType_t xAccReturned;
	BaseType_t xGyroReturned;
	BaseType_t xPrintReturned;

	//task for magnetometer
	xMagReturned = xTaskCreate(
	vTaskMagnetometer, 					/* Function that implements the task. */
	"Magnetometer", 					/* Text name for the task. */
	512, 								/* Stack size in words, not bytes. */
	(void*) 1, 							/* Parameter passed into the task. */
	3, 									/* Priority at which the task is created. */
	&xMagHandle); 						/* Used to pass out the created task's handle. */

	if (xMagReturned != pdPASS) {
		printf("failed to create Magnetometer\n");
	}

	//task for accelometer
	xAccReturned = xTaskCreate(
	vTaskAccel,  						/* Function that implements the task. */
	"Pospeskometer", 					/* Text name for the task. */
	512, 								/* Stack size in words, not bytes. */
	(void*) 1, 							/* Parameter passed into the task. */
	3, 									/* Priority at which the task is created. */
	&xAccHandle); 						/* Used to pass out the created task's handle. */

	if (xAccReturned != pdPASS) {
		printf("failed to create Accel\n");
	}

	//task for gyro
	xGyroReturned = xTaskCreate(
	vTaskGyro, 							/* Function that implements the task. */
	"Gyroskop",							/* Text name for the task. */
	512, 								/* Stack size in words, not bytes. */
	(void*) 1, 							/* Parameter passed into the task. */
	3, 									/* Priority at which the task is created. */
	&xGyroHandle); 						/* Used to pass out the created task's handle. */

	if (xGyroReturned != pdPASS) {
		printf("failed to create Gyro\n");
	}

	//task for cdc transmit
	xPrintReturned = xTaskCreate(
	vTaskPrint, 						/* Function that implements the task. */
	"Transmit", 						/* Text name for the task. */
	512, 								/* Stack size in words, not bytes. */
	(void*) 1, 							/* Parameter passed into the task. */
	3, 									/* Priority at which the task is created. */
	&xPrintHandle); 					/* Used to pass out the created task's handle. */

	if (xPrintReturned != pdPASS) {
		printf("failed to create Transmit\n");
	}

	vTaskSuspend(xAccHandle);
	vTaskSuspend(xMagHandle);

	xQueue = xQueueCreate(9, sizeof(float));

	/* USER CODE END 2 */

	/* USER CODE BEGIN RTOS_MUTEX */
	/* add mutexes, ... */
	/* USER CODE END RTOS_MUTEX */

	/* USER CODE BEGIN RTOS_SEMAPHORES */
	/* add semaphores, ... */
	/* USER CODE END RTOS_SEMAPHORES */

	/* USER CODE BEGIN RTOS_TIMERS */
	/* start timers, add new ones, ... */
	/* USER CODE END RTOS_TIMERS */

	/* USER CODE BEGIN RTOS_QUEUES */
	/* add queues, ... */
	/* USER CODE END RTOS_QUEUES */

	/* Create the thread(s) */
	/* definition and creation of defaultTask */
	osThreadDef(defaultTask, StartDefaultTask, osPriorityNormal, 0, 128);
	defaultTaskHandle = osThreadCreate(osThread(defaultTask), NULL);

	/* USER CODE BEGIN RTOS_THREADS */
	/* add threads, ... */
	/* USER CODE END RTOS_THREADS */

	/* Start scheduler */
	osKernelStart();

	/* We should never get here as control is now taken by the scheduler */
	/* Infinite loop */
	/* USER CODE BEGIN WHILE */
	while (1) {
		/* USER CODE END WHILE */

		/* USER CODE BEGIN 3 */
	}
	/* USER CODE END 3 */
}

/**
 * @brief System Clock Configuration
 * @retval None
 */
void SystemClock_Config(void) {
	RCC_OscInitTypeDef RCC_OscInitStruct = { 0 };
	RCC_ClkInitTypeDef RCC_ClkInitStruct = { 0 };
	RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = { 0 };

	/** Configure the main internal regulator output voltage
	 */
	__HAL_RCC_PWR_CLK_ENABLE();
	__HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
	/** Initializes the RCC Oscillators according to the specified parameters
	 * in the RCC_OscInitTypeDef structure.
	 */
	RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
	RCC_OscInitStruct.HSEState = RCC_HSE_ON;
	RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
	RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
	RCC_OscInitStruct.PLL.PLLM = 4;
	RCC_OscInitStruct.PLL.PLLN = 168;
	RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
	RCC_OscInitStruct.PLL.PLLQ = 7;
	if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
		Error_Handler();
	}
	/** Initializes the CPU, AHB and APB buses clocks
	 */
	RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
			| RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
	RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
	RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
	RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
	RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

	if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK) {
		Error_Handler();
	}
	PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_I2S;
	PeriphClkInitStruct.PLLI2S.PLLI2SN = 200;
	PeriphClkInitStruct.PLLI2S.PLLI2SM = 5;
	PeriphClkInitStruct.PLLI2S.PLLI2SR = 2;
	if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK) {
		Error_Handler();
	}
}

/**
 * @brief I2C1 Initialization Function
 * @param None
 * @retval None
 */
static void MX_I2C1_Init(void) {

	/* USER CODE BEGIN I2C1_Init 0 */

	/* USER CODE END I2C1_Init 0 */

	/* USER CODE BEGIN I2C1_Init 1 */

	/* USER CODE END I2C1_Init 1 */
	hi2c1.Instance = I2C1;
	hi2c1.Init.ClockSpeed = 400000;
	hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_16_9;
	hi2c1.Init.OwnAddress1 = 0;
	hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
	hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
	hi2c1.Init.OwnAddress2 = 0;
	hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
	hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
	if (HAL_I2C_Init(&hi2c1) != HAL_OK) {
		Error_Handler();
	}
	/* USER CODE BEGIN I2C1_Init 2 */

	/* USER CODE END I2C1_Init 2 */

}

/**
 * @brief I2S2 Initialization Function
 * @param None
 * @retval None
 */
static void MX_I2S2_Init(void) {

	/* USER CODE BEGIN I2S2_Init 0 */

	/* USER CODE END I2S2_Init 0 */

	/* USER CODE BEGIN I2S2_Init 1 */

	/* USER CODE END I2S2_Init 1 */
	hi2s2.Instance = SPI2;
	hi2s2.Init.Mode = I2S_MODE_MASTER_TX;
	hi2s2.Init.Standard = I2S_STANDARD_PHILIPS;
	hi2s2.Init.DataFormat = I2S_DATAFORMAT_16B;
	hi2s2.Init.MCLKOutput = I2S_MCLKOUTPUT_DISABLE;
	hi2s2.Init.AudioFreq = I2S_AUDIOFREQ_96K;
	hi2s2.Init.CPOL = I2S_CPOL_LOW;
	hi2s2.Init.ClockSource = I2S_CLOCK_PLL;
	hi2s2.Init.FullDuplexMode = I2S_FULLDUPLEXMODE_ENABLE;
	if (HAL_I2S_Init(&hi2s2) != HAL_OK) {
		Error_Handler();
	}
	/* USER CODE BEGIN I2S2_Init 2 */

	/* USER CODE END I2S2_Init 2 */

}

/**
 * @brief I2S3 Initialization Function
 * @param None
 * @retval None
 */
static void MX_I2S3_Init(void) {

	/* USER CODE BEGIN I2S3_Init 0 */

	/* USER CODE END I2S3_Init 0 */

	/* USER CODE BEGIN I2S3_Init 1 */

	/* USER CODE END I2S3_Init 1 */
	hi2s3.Instance = SPI3;
	hi2s3.Init.Mode = I2S_MODE_MASTER_TX;
	hi2s3.Init.Standard = I2S_STANDARD_PHILIPS;
	hi2s3.Init.DataFormat = I2S_DATAFORMAT_16B;
	hi2s3.Init.MCLKOutput = I2S_MCLKOUTPUT_ENABLE;
	hi2s3.Init.AudioFreq = I2S_AUDIOFREQ_96K;
	hi2s3.Init.CPOL = I2S_CPOL_LOW;
	hi2s3.Init.ClockSource = I2S_CLOCK_PLL;
	hi2s3.Init.FullDuplexMode = I2S_FULLDUPLEXMODE_DISABLE;
	if (HAL_I2S_Init(&hi2s3) != HAL_OK) {
		Error_Handler();
	}
	/* USER CODE BEGIN I2S3_Init 2 */

	/* USER CODE END I2S3_Init 2 */

}

/**
 * @brief SPI1 Initialization Function
 * @param None
 * @retval None
 */
static void MX_SPI1_Init(void) {

	/* USER CODE BEGIN SPI1_Init 0 */

	/* USER CODE END SPI1_Init 0 */

	/* USER CODE BEGIN SPI1_Init 1 */

	/* USER CODE END SPI1_Init 1 */
	/* SPI1 parameter configuration*/
	hspi1.Instance = SPI1;
	hspi1.Init.Mode = SPI_MODE_MASTER;
	hspi1.Init.Direction = SPI_DIRECTION_2LINES;
	hspi1.Init.DataSize = SPI_DATASIZE_8BIT;
	hspi1.Init.CLKPolarity = SPI_POLARITY_HIGH;
	hspi1.Init.CLKPhase = SPI_PHASE_2EDGE;
	hspi1.Init.NSS = SPI_NSS_SOFT;
	hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_16;
	hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;
	hspi1.Init.TIMode = SPI_TIMODE_DISABLE;
	hspi1.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;
	hspi1.Init.CRCPolynomial = 10;
	if (HAL_SPI_Init(&hspi1) != HAL_OK) {
		Error_Handler();
	}
	/* USER CODE BEGIN SPI1_Init 2 */

	/* USER CODE END SPI1_Init 2 */

}

/**
 * @brief GPIO Initialization Function
 * @param None
 * @retval None
 */
static void MX_GPIO_Init(void) {
	GPIO_InitTypeDef GPIO_InitStruct = { 0 };

	/* GPIO Ports Clock Enable */
	__HAL_RCC_GPIOE_CLK_ENABLE();
	__HAL_RCC_GPIOC_CLK_ENABLE();
	__HAL_RCC_GPIOH_CLK_ENABLE();
	__HAL_RCC_GPIOA_CLK_ENABLE();
	__HAL_RCC_GPIOB_CLK_ENABLE();
	__HAL_RCC_GPIOD_CLK_ENABLE();

	/*Configure GPIO pin Output Level */
	HAL_GPIO_WritePin(CS_I2C_SPI_GPIO_Port, CS_I2C_SPI_Pin, GPIO_PIN_RESET);

	/*Configure GPIO pin Output Level */
	HAL_GPIO_WritePin(OTG_FS_PowerSwitchOn_GPIO_Port, OTG_FS_PowerSwitchOn_Pin,
			GPIO_PIN_SET);

	/*Configure GPIO pin Output Level */
	HAL_GPIO_WritePin(GPIOD,
			LD4_Pin | LD3_Pin | LD5_Pin | LD6_Pin | Audio_RST_Pin,
			GPIO_PIN_RESET);

	/*Configure GPIO pin : DATA_Ready_Pin */
	GPIO_InitStruct.Pin = DATA_Ready_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(DATA_Ready_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : CS_I2C_SPI_Pin */
	GPIO_InitStruct.Pin = CS_I2C_SPI_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
	HAL_GPIO_Init(CS_I2C_SPI_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pins : INT1_Pin INT2_Pin MEMS_INT2_Pin */
	GPIO_InitStruct.Pin = INT1_Pin | INT2_Pin | MEMS_INT2_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_EVT_RISING;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);

	/*Configure GPIO pin : OTG_FS_PowerSwitchOn_Pin */
	GPIO_InitStruct.Pin = OTG_FS_PowerSwitchOn_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	HAL_GPIO_Init(OTG_FS_PowerSwitchOn_GPIO_Port, &GPIO_InitStruct);

	/*Configure GPIO pin : PA0 */
	GPIO_InitStruct.Pin = GPIO_PIN_0;
	GPIO_InitStruct.Mode = GPIO_MODE_EVT_RISING;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

	/*Configure GPIO pins : LD4_Pin LD3_Pin LD5_Pin LD6_Pin
	 Audio_RST_Pin */
	GPIO_InitStruct.Pin = LD4_Pin | LD3_Pin | LD5_Pin | LD6_Pin | Audio_RST_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

	/*Configure GPIO pin : OTG_FS_OverCurrent_Pin */
	GPIO_InitStruct.Pin = OTG_FS_OverCurrent_Pin;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	HAL_GPIO_Init(OTG_FS_OverCurrent_GPIO_Port, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/* USER CODE BEGIN Header_StartDefaultTask */
/**
 * @brief  Function implementing the defaultTask thread.
 * @param  argument: Not used
 * @retval None
 */
/* USER CODE END Header_StartDefaultTask */
void StartDefaultTask(void const *argument) {
	/* init code for USB_DEVICE */
	MX_USB_DEVICE_Init();
	/* USER CODE BEGIN 5 */
	/* Infinite loop */
	for (;;) {
		osDelay(1);
	}
	/* USER CODE END 5 */
}

/**
 * @brief  This function is executed in case of error occurrence.
 * @retval None
 */
void Error_Handler(void) {
	/* USER CODE BEGIN Error_Handler_Debug */
	/* User can add his own implementation to report the HAL error return state */

	/* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
