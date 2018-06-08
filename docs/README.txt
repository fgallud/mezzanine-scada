This is a set of apps for mezzanine that turns mezzanine into a scada system

- mezzanine_scada_base run the threads needed for the other apps and contains
  a real time database  thread-safe and mechanism to sync the different
  threads. For example, a thread that controls the temperature in an oven can
  sleep until a new temperature value is available

- mezzanine_scada_hardware do the measurements and write the data into the
  realtime database. It also do the oposite task. If one thread write a new
  value in the database that is an output value, it takes this value into
  the real world by writting it into the correct output hardware.
  It also contains software simulated hardware. This allow us to write a
  simulation of the system we are going to control and write the code
  without real hardware. This is important if the real hardware is slow,
  costly to operate or if it can catch fire if the software fails.

- mezzanine_scada_state_machine is a state machine control system

- mezzanine_scada_register is the app that saves the data every now and then
  to file records. This allow us to see the evolution of variables over time

- mezzanine_scada_gui is the app that provides the resources to turn
  mezzanine into a scada grafical user interface. It can plot charts, show
  schematics of the system, change the state of the system by clicking into
  the schematic elements and so on


