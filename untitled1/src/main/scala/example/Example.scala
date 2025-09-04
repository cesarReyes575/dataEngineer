package example

import scala.io.StdIn.readLine

class Example {

  val numNat: List[Int] = (1 to 100).toList
///////////
  def validaEntero(numero: String): Boolean = {
    /*recibe string y regresa boleano*/ if (numero.isEmpty)//si es vacio regresa falso
      false
    else {             //caso contrario
      val numero2 =
        if (numero.startsWith("-"))
          numero.tail
        else
          numero
      numero2.nonEmpty && numero2.forall(_.isDigit)//forall--> valida si es verdadero rgresa true isDigit valida si la cadena es numero
    }
  }
////////
  def contieneNumero(numero: String): Boolean =  {
    val numero2 = numero.toInt
    if(numNat.contains(numero2) && numero2 <=100 && numero2 > 0)
      true
    else
      false
  }

  def Extract(numero:String): Option[Int] = {
    val numero2 = numero.toInt
    numNat.find(_ == numero2)
  }

  ////////////
}


object Example {

  def main(args: Array[String]): Unit = {

    val conjunto = new Example()
    println("Ingresa un número entero:")
    val entrada = readLine()
    if (conjunto.validaEntero(entrada)) {
      println("es numero -->")
      if (conjunto.contieneNumero(entrada))
        println("--->si exite")
        val resultado = conjunto.Extract(entrada)
        print("el numero extraido es ",resultado)
      else println("no existe o fuera de rango <1 a 100>")
    } else {
      println("Error: Debes ingresar un número.")
    }

  }
}
