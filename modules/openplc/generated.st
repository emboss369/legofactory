PROGRAM Test
  VAR
    my_button AT %IX0.25 : BOOL;
    lamp AT %QX0.15 : BOOL;
  END_VAR

  lamp := my_button;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : Hello_World;
  END_RESOURCE
END_CONFIGURATION
