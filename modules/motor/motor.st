PROGRAM PLC_PRG
VAR
    motorRun : BOOL := FALSE;             // モーター動作フラグ
    rotateDir : INT := 1;                 // 回転方向（+1: 正転, -1: 逆転）
    stepIndex : INT := 0;                 // ステップインデックス
    delayTime : TIME := T#1ms;            // ステップ間の遅延時間
    stepTimer : TON;                          // タイマーFBのインスタンス

    stepPatterns : ARRAY[0..7] OF BYTE := [
        16#01,  // OUT1
        16#03,  // OUT1 + OUT2
        16#02,  // OUT2
        16#06,  // OUT2 + OUT3
        16#04,  // OUT3
        16#0C,  // OUT3 + OUT4
        16#08,  // OUT4
        16#09   // OUT4 + OUT1
    ];

    // GPIOマッピング（ビット番号に対応）
    OUT1 AT %QX2.1 : BOOL := FALSE;  // GPIO17
    OUT2 AT %QX3.3 : BOOL := FALSE;  // GPIO27
    OUT3 AT %QX2.6 : BOOL := FALSE;  // GPIO22
    OUT4 AT %QX2.7 : BOOL := FALSE;  // GPIO23
END_VAR

// === 実行サイクルごとの処理 ===

// タイマー入力の設定
stepTimer.IN := motorRun;
stepTimer.PT := delayTime;
stepTimer(); // タイマーの実行

IF motorRun THEN
    IF stepTimer.Q THEN
        // タイマーのトリガーを検出したら、次のステップへ
        stepTimer.IN := FALSE;  // タイマーのリセット（次回再起動のため）

        // ステップインデックスの更新（正転/逆転対応）
        stepIndex := (stepIndex + rotateDir + 8) MOD 8;

        // ビットパターンから出力を設定
        OUT1 := (stepPatterns[stepIndex] AND 16#01) <> 0;
        OUT2 := (stepPatterns[stepIndex] AND 16#02) <> 0;
        OUT3 := (stepPatterns[stepIndex] AND 16#04) <> 0;
        OUT4 := (stepPatterns[stepIndex] AND 16#08) <> 0;
    END_IF;
ELSE
    // モーター停止時：すべての出力をOFF
    OUT1 := FALSE;
    OUT2 := FALSE;
    OUT3 := FALSE;
    OUT4 := FALSE;
END_IF;
