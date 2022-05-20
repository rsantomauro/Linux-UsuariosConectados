#!/bin/bash
# Funcion para convertir las horas en minutos
horas2min() {
	MINUTOS=$(($1 * 60))
}
#
# Funcion para convertir el promedio de horas y minutos total
min2HyMTotal() {
	HORATOTAL=$(($1 / 60))
	MINTOTAL=$(($1 % 60))
}
# Funcion para convertir horas en dias
horas2days() {
	DIASTOTAL=$(($1 / 24))
	HORATOTAL=$(($1 % 60))
}
#
#Por defecto no muestra el tiempo total de conexion
RESULT=false
#
if [ $# -gt 3 ]; then
	echo "Cantidad de parametros erronea, solo se aceptan los modificadores -r y -u (seguido de un nombre de usuario)." >&2
	exit 3
fi
# Obtengo parametros y los asignos a variables
while getopts u:r flag
do
	case "${flag}" in
		u) USUARIO=${OPTARG};;
		r) RESULT=true;;
		*) echo "Modificador $OPTARG incorrecto. Solo se aceptan -r y -u usuario, y en ese orden en caso de estar ambos presentes." >&2			;exit 4;;
	esac
done
#done 2>> /etc/null
#
# Valido los parametros
# Busqueda por usuario
# Validamos que se haya ingresado el modificador usuario
if ! [ -z $USUARIO ] && [ $USUARIO != "-r" ]; then
	# Si se ingreso un modificador se filtra el comando last con el mismo
	echo -e "Usuario\t Term\t      Host\t       Fecha\t  H.Con\t  H.Des\t T.Con"
	last | grep '([0-2][0-9]:[0-5][0-9])' | grep $USUARIO
	#echo "
#"
	# En caso que se haya ingresado el modificador -r
	if "$RESULT"; then
		# Sumo horas, se lo puede pasar a funcion
		TOTAL=0	
		for hora in `last | grep '([0-2][0-9]:[0-5][0-9])' | grep $USUARIO | tr -s [:space:] | cut -d " " -f10 | tr -d "(" | tr -d ")" | cut -d ":" -f 1`; do
			# Se agrega 10# para que asuma que es en base 10 y no en octal(este cambio se hace porque al comenzar con 0 interpreta octal)
			TOTAL=$((10#$TOTAL + 10#$hora))	
		done
		# Convierto las horas a minutos
		horas2min $TOTAL

		# Sumo minutos, se lo puede pasar a funcion
		TOTAL=0
                for minuto in `last | grep '([0-2][0-9]:[0-5][0-9])' | grep $USUARIO | tr -s [:space:] | cut -d " " -f10 | tr -d "(" | tr -d ")" | cut -d ":" -f 2`; do
                        # Se agrega 10# para que asuma que es en base 10 y no en octal(este cambio se hace porque al comenzar con 0 interpreta octal)
                        TOTAL=$((10#$TOTAL + 10#$minuto))
                done
		MINUTOS=$((10#$MINUTOS + 10#$TOTAL))

		# Convierto los minutos en horas y minutos
		min2HyMTotal $MINUTOS
		
		if [ $HORATOTAL -gt 59 ]; then
			# Muestra las hora y minutos totales
			horas2days $HORATOTAL
			echo -e "\nEl tiempo total de conexion es: $DIASTOTAL dias, $HORATOTAL horas y $MINTOTAL minutos."
		else
			echo -e "\nEl tiempo total de conexion es: $HORATOTAL horas y $MINTOTAL minutos."
		
		fi
	fi
else
	# Cuando no se ingresa valores para el modificador -u devuelve el siguiente mensaje
	echo "No se ha especificado el usuario para el modificador -u." >&2
	exit 1
fi

#echo -e "Usuario\t Term\t Host\t Fecha\tH.Con\tH.Des\tT.Con"
#printf "Usuario Term Host Fecha H.Con H.Des T.Con"
#last | grep '([0-2][0-9]:[0-5][0-9])' | grep $USUARIO